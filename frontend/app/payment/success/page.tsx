"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function SuccessPage() {
  return (
    <div className="max-w-xl mx-auto text-center space-y-6">
      <h1 className="text-4xl font-bold">
        Payment Successful
      </h1>

      <p>
        Your subscription has been activated.
      </p>

      <Link href="/billing">
        <Button>
          Back to Billing
        </Button>
      </Link>
    </div>
  );
}