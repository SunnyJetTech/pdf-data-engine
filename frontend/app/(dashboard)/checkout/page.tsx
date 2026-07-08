"use client";

import { createCheckout } from "@/api/subscription.api";
import { Button } from "@/components/ui/button";
import { notify } from "@/lib/notify";

export default function CheckoutPage() {

  async function handleUpgrade() {
    try {
      const res =
        await createCheckout("pro");

      if (
        res.status === "success" &&
        res.data?.authorization_url
      ) {
        window.location.href =
          res.data.authorization_url;
      }
    } catch (err) {
      notify.error(err);
    }
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">
        Upgrade Plan
      </h1>

      <div className="border rounded-lg p-6">
        <h2 className="font-bold text-xl">
          Pro Plan
        </h2>

        <p>
          Unlimited uploads,
          searches and exports.
        </p>

        <Button
          className="mt-4"
          onClick={handleUpgrade}
        >
          Pay with Paystack
        </Button>
      </div>
    </div>
  );
}