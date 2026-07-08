"use client";

import { useState } from "react";
import {useSearchParams, useRouter,} from "next/navigation";
import { resetPassword } from "@/api/auth.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { notify } from "@/lib/notify";

export default function ResetPasswordPage() {
  const router = useRouter();
  const params = useSearchParams();
  const token = params.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword,] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleReset() {
    if (
      password.trim() !==
      confirmPassword.trim()
    ) {
      notify.error(
        "Passwords do not match"
      );
      return;
    }

    setLoading(true);

    try {
      const res = await resetPassword(token, {password, confirmPassword});

      if (res.status === "success") {
        notify.success(
          "Password reset successfully"
        );

        router.push("/login");
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
        Reset Password
      </h1>

      <Input
        type="password"
        placeholder="New password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <Input
        type="password"
        placeholder="Confirm password"
        value={confirmPassword}
        onChange={(e) =>
          setConfirmPassword(
            e.target.value
          )
        }
      />

      <Button
        onClick={handleReset}
        disabled={loading}
        className="w-full"
      >
        {loading
          ? "Resetting..."
          : "Reset Password"}
      </Button>
    </div>
  );
}