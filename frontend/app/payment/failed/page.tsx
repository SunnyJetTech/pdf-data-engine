"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function FailedPage() {
  return (
    <div className="max-w-xl mx-auto text-center space-y-6">
      <h1 className="text-4xl font-bold">
        Payment Failed
      </h1>

      <p>
        Your payment was not completed.
      </p>

      <Link href="/checkout">
        <Button>
          Try Again
        </Button>
      </Link>
    </div>
  );
}