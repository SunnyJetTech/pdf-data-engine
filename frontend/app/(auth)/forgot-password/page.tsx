"use client";

import { useState } from "react";
import Link from "next/link";

import { forgotPassword } from "@/api/auth.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { notify } from "@/lib/notify";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    if (!email.trim()) {
      notify.error("Email is required");
      return;
    }

    setLoading(true);

    try {
      const res = await forgotPassword({
        email,
      });

      if (res.status === "success") {
        notify.success(
          "Reset link sent to your email"
        );

        setEmail("");
      }
    } catch (err) {
      notify.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h1 className="text-2xl font-bold">
        Forgot Password
      </h1>

      <Input
        placeholder="Email address"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <Button
        onClick={handleSubmit}
        disabled={loading}
        className="w-full"
      >
        {loading
          ? "Sending..."
          : "Send Reset Link"}
      </Button>

      <div className="text-sm flex justify-between">
        <Link
          href="/login"
          className="text-primary"
        >
          Login
        </Link>

        <Link
          href="/register"
          className="text-primary"
        >
          Register
        </Link>
      </div>
    </div>
  );
}