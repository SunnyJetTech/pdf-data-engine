"use client";

import { useEffect, useState } from "react";
import { getSubscription } from "@/api/subscription.api";
import { Button } from "@/components/ui/button";
import { notify } from "@/lib/notify";

export default function BillingPage() {
  const [subscription, setSubscription] =
    useState<any>(null);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      const res =
        await getSubscription();

      if (
        res.status === "success" &&
        res.data
      ) {
        setSubscription(res.data);
      }
    } catch (err) {
      notify.error(err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <p>Loading billing...</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Billing
      </h1>

      <div className="border rounded-lg p-6">
        <p>
          <strong>Plan:</strong>{" "}
          {subscription?.plan || "Free"}
        </p>

        <p>
          <strong>Status:</strong>{" "}
          {subscription?.status || "Inactive"}
        </p>

        <p>
          <strong>Expires:</strong>{" "}
          {subscription?.expires_at ||
            "N/A"}
        </p>
      </div>

      <Button
        onClick={() =>
          window.location.href =
            "/checkout"
        }
      >
        Upgrade Plan
      </Button>
    </div>
  );
}