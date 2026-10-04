from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from auth.password_manager import password_hash
from core.constants.activity import ActivityAction
from core.constants.subscription import SubscriptionStatus
from core.models.pricing_plan import PricingPlan
from core.models.quota import Quota
from core.models.subscription import Subscription
from core.models.tenant import Tenant
from core.models.tenant_member import TenantMember
from core.models.usage import Usage
from core.models.user import User
from repositories.pricing_plan_repository import PricingPlanRepository
from repositories.quota_repository import QuotaRepository
from repositories.subscription_repository import SubscriptionRepository
from repositories.tenant_member_repository import TenantMemberRepository
from repositories.tenant_repository import TenantRepository
from repositories.usage_repository import UsageRepository
from repositories.user_repository import UserRepository
from services.activity_service import ActivityService
from services.authorization_service import AuthorizationService
from services.mail_service import MailService


class OnboardingService:
    def __init__(self, db: Session) -> None:
        self.db = db

        self.users = UserRepository(db)
        self.tenants = TenantRepository(db)
        self.members = TenantMemberRepository(db)
        self.quotas = QuotaRepository(db)
        self.usage = UsageRepository(db)
        self.subscriptions = SubscriptionRepository(db)
        self.pricing = PricingPlanRepository(db)

        self.activity = ActivityService(db)
        self.authorization = AuthorizationService(db)

    async def create_account(self, *, payload) -> User:

        if self.users.by_email(email=payload.email):
            raise ValueError("Email already exists.")

        if self.users.by_username(username=payload.username):
            raise ValueError("Username already exists.")

        free_plan: PricingPlan | None = self.pricing.free_plan()

        if free_plan is None:
            raise ValueError("No free pricing plan configured.")

        try:
            user = User(
                username=payload.username,
                email=payload.email,
                password_hash=password_hash(payload.password),
                first_name=payload.first_name,
                last_name=payload.last_name,
                is_active=True,
                is_verified=False,
            )

            self.users.add(user)

            self.db.flush()

            tenant = Tenant(
                owner_id=user.id,
                name=f"{user.username}'s Workspace",
                slug=self.tenants.generate_unique_slug(f"{user.username} workspace"),
            )

            self.tenants.add(tenant)

            self.db.flush()

            user.current_tenant_id = tenant.id

            owner_role = self.authorization.ensure_owner_role(tenant_id=tenant.id)

            membership = TenantMember(tenant_id=tenant.id, user_id=user.id, role_id=owner_role.id, accepted_at=datetime.utcnow())

            self.members.add(membership)

            usage = Usage(tenant_id=tenant.id)

            self.usage.add(usage)

            quota = Quota(
                tenant_id=tenant.id,
                datasets_limit=free_plan.datasets_limit,
                documents_limit=free_plan.documents_limit,
                searches_limit=free_plan.searches_limit,
                chat_messages_limit=free_plan.chat_messages_limit,
                exports_limit=free_plan.exports_limit,
                storage_limit_mb=free_plan.storage_limit_mb,
                ai_tokens_limit=free_plan.ai_tokens_limit,
            )

            self.quotas.add(quota)

            starts_at = datetime.utcnow()

            subscription = Subscription(
                tenant_id=tenant.id,
                plan_id=free_plan.id,
                status=SubscriptionStatus.ACTIVE,
                starts_at=starts_at,
                expires_at=(starts_at + timedelta(days=free_plan.duration_days)),
                auto_renew=False,
            )

            self.subscriptions.add(subscription)

            self.activity.log(user_id=user.id, action=ActivityAction.USER_CREATED)

            self.db.flush()
            self.db.commit()

            self.db.refresh(user)

        except Exception:
            self.db.rollback()
            raise

        await MailService.send_welcome_email( recipient=user.email, username=user.username)

        return user