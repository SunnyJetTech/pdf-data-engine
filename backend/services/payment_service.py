from __future__ import annotations
import secrets
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.constants.payment import PaymentProvider, PaymentStatus
from core.models.payment import Payment
from core.models.pricing_plan import PricingPlan
from core.models.tenant import Tenant
from repositories.payment_repository import PaymentRepository
from repositories.pricing_plan_repository import PricingPlanRepository
from payment.flutterwave_service import FlutterwaveService
from payment.money import to_minor_units
from payment.paystack_service import PaystackService
from payment.stripe_service import StripeService
from subscription.subscription_service import SubscriptionService

class PaymentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.payments = PaymentRepository(db)
        self.plans = PricingPlanRepository(db)
        self.subscriptions = SubscriptionService(db)

    @staticmethod
    def _provider_service(provider: PaymentProvider) -> Any:
        services = {
            PaymentProvider.PAYSTACK: PaystackService,
            PaymentProvider.STRIPE: StripeService,
            PaymentProvider.FLUTTERWAVE: FlutterwaveService,
        }

        service = services.get(provider)

        if service is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported payment provider.")

        return service

    def by_id(self, payment_id: UUID) -> Payment:
        payment = self.payments.by_id(payment_id)

        if payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Payment not found.")

        return payment

    def by_reference(self, reference: str) -> Payment:
        payment = self.payments.by_reference(reference)

        if payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")

        return payment

    def latest(self, tenant_id: UUID) -> Payment | None:
        return self.payments.latest(tenant_id)

    def history(self, tenant_id: UUID) -> list[Payment]:
        return self.payments.by_tenant(tenant_id)

    def pending(self) -> list[Payment]:
        return self.payments.pending()


    def create(self, *, tenant: Tenant, plan: PricingPlan, provider: PaymentProvider, reference: str) -> Payment:
        if not plan.active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This pricing plan is not available.")

        if self.payments.exists_reference(reference):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate payment reference.")

        payment = Payment(
            tenant_id=tenant.id,
            pricing_plan_id=plan.id,
            amount=plan.amount,
            currency=plan.currency.upper(),
            provider=provider,
            reference=reference,
            status=PaymentStatus.PENDING,
        )

        try:
            self.payments.add(payment)
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            raise

        return payment

    def initialize_payment(self, *, tenant: Tenant, plan: PricingPlan, provider: PaymentProvider, email: str) -> dict[str, Any]:
        reference = f"ds_{secrets.token_urlsafe(24)}"

        payment = self.create(tenant=tenant, plan=plan, provider=provider, reference=reference)
        provider_service = self._provider_service(provider)

        try:
            result = provider_service.initialize_payment(
                email=email,
                amount=payment.amount,
                currency=payment.currency,
                reference=payment.reference,
                metadata={
                    "payment_id": str(payment.id),
                    "tenant_id": str(tenant.id),
                    "pricing_plan_id": str(plan.id),
                },
            )

            if provider == PaymentProvider.PAYSTACK:
                checkout_url = PaystackService.authorization_url(result)

            elif provider == PaymentProvider.STRIPE:
                checkout_url = result.get("url")

                session_id = result.get("id")
                if not session_id or not checkout_url:
                    raise ValueError("Stripe did not return a valid Checkout Session.")

                payment.transaction_id = session_id
                self.db.commit()

            else:
                checkout_url = result.get("data", {}).get("link")

            if not isinstance(checkout_url, str) or not checkout_url:
                raise ValueError("The payment provider did not return a checkout URL.")

        except Exception as exc:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "Payment initialization could not be confirmed. "
                    "The payment remains pending until its provider "
                    "status can be reconciled."
                ),
            ) from exc

        return {
            "payment_id": str(payment.id),
            "reference": payment.reference,
            "provider": payment.provider.value,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status.value,
            "checkout_url": checkout_url,
        }

    def mark_success(self, *, payment: Payment, transaction_id: str) -> Payment:
        if payment.status == PaymentStatus.SUCCESS:
            return payment

        if payment.status != PaymentStatus.PENDING:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="Only pending payments can be marked successful.")

        try:
            self.payments.mark_success( payment, transaction_id=transaction_id)
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            raise

        return payment

    def mark_failed(self, *, payment: Payment) -> Payment:
        if payment.status != PaymentStatus.PENDING:
            return payment

        try:
            self.payments.mark_failed(payment)
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            raise

        return payment

    def cancel(self, payment: Payment) -> Payment:
        if payment.status != PaymentStatus.PENDING:
            return payment

        try:
            self.payments.mark_cancelled(payment)
            self.db.commit()
            self.db.refresh(payment)
        except Exception:
            self.db.rollback()
            raise

        return payment

    def verify_payment(self, *, reference: str, tenant_id: UUID, provider_transaction_id: str | None = None) -> Payment:
        stmt = select(Payment).where( Payment.reference == reference, Payment.tenant_id == tenant_id).with_for_update()
        payment = self.db.scalar(stmt)

        if payment is None:
            raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found.")

        if payment.status == PaymentStatus.SUCCESS:
            return payment

        if payment.status != PaymentStatus.PENDING:
            raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="This payment is no longer pending.")

        try:
            if payment.provider == PaymentProvider.PAYSTACK:
                result = PaystackService.verify_payment(reference=payment.reference)
                data = result.get("data", {})

                successful = PaystackService.payment_successful(result)
                verified_reference = data.get("reference")
                verified_amount = data.get("amount")
                verified_currency = data.get("currency")
                transaction_id = str(data.get("id") or "")

                expected_amount = to_minor_units(payment.amount, payment.currency)

            elif payment.provider == PaymentProvider.STRIPE:
                session_id = (payment.transaction_id or provider_transaction_id)

                if not session_id:
                    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Stripe Checkout Session ID is required.")

                result = StripeService.verify_payment(session_id=session_id)
                successful = StripeService.payment_successful(result)

                verified_reference = (result.get("client_reference_id") or result.get("metadata", {}).get("reference"))
                verified_amount = result.get("amount_total")
                verified_currency = result.get("currency")
                transaction_id = StripeService.transaction_id(result)

                expected_amount = to_minor_units(payment.amount, payment.currency)

            elif payment.provider == PaymentProvider.FLUTTERWAVE:
                if not provider_transaction_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flutterwave transaction ID is required.")

                result = FlutterwaveService.verify_payment(transaction_id=provider_transaction_id)
                data = FlutterwaveService.transaction_data(result)

                successful = FlutterwaveService.payment_successful(result)
                verified_reference = data.get("tx_ref")
                verified_amount = data.get("amount")
                verified_currency = data.get("currency")
                transaction_id = str(data.get("id") or "")

                expected_amount = Decimal(str(payment.amount))

            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported payment provider.")

            if not successful:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The provider has not confirmed a successful payment.")

            if verified_reference != payment.reference:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment reference does not match.")

            if not transaction_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provider transaction ID is missing.")

            if (not isinstance(verified_currency, str)  or verified_currency.upper() != payment.currency.upper()):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment currency does not match.")

            try:
                if payment.provider in ( PaymentProvider.PAYSTACK, PaymentProvider.STRIPE):
                    actual_amount = Decimal(str(verified_amount))
                    amount_matches = (
                        actual_amount.is_finite()
                        and actual_amount == actual_amount.to_integral_value()
                        and actual_amount == Decimal(expected_amount)
                    )
                else:
                    actual_amount = Decimal(str(verified_amount))
                    amount_matches = (actual_amount.is_finite() and actual_amount == expected_amount)
            except (InvalidOperation, TypeError, ValueError):
                amount_matches = False

            if not amount_matches:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment amount does not match.")

            plan = self.plans.by_id(payment.pricing_plan_id)

            if plan is None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The payment pricing plan could not be found.")

            if (plan.amount != payment.amount  or plan.currency.upper() != payment.currency.upper()):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The stored payment does not match its pricing plan.")

            subscription = self.subscriptions.current(payment.tenant_id)

            if subscription is None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No subscription exists for this tenant.")

            self.subscriptions.change_plan( subscription=subscription, plan=plan)
            self.payments.mark_success( payment, transaction_id=transaction_id)
            payment.subscription_id = subscription.id

            self.db.commit()
            self.db.refresh(payment)

            return payment

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unable to verify payment with the provider.") from exc

    def verify_success(self, *, payment: Payment, transaction_id: str, plan: PricingPlan) -> Payment:

        stored_payment = self.by_id(payment.id)

        if stored_payment.status == PaymentStatus.SUCCESS:
            return stored_payment

        if stored_payment.reference != payment.reference:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment reference mismatch.")

        stored_plan = self.plans.by_id(stored_payment.pricing_plan_id)

        if stored_plan is None or stored_plan.id != plan.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pricing plan does not match the payment.")

        return self.verify_payment(
            reference=stored_payment.reference,
            tenant_id=stored_payment.tenant_id,
            provider_transaction_id=(transaction_id if stored_payment.provider == PaymentProvider.FLUTTERWAVE  else None),
        )

    def total_successful_amount(self, tenant_id: UUID) -> int:
        return self.payments.total_successful_amount(tenant_id)

    def successful_count(self, tenant_id: UUID) -> int:
        return self.payments.count_successful(tenant_id)
