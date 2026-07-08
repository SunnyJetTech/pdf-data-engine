"use client";

import { useState } from "react";
import { changePassword } from "@/api/auth.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { notify } from "@/lib/notify";

export default function ChangePasswordPage() {
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleChange() {
    if (
      !password.trim() ||
      !newPassword.trim() ||
      !confirmNewPassword.trim()
    ) {
      notify.error("All fields are required");
      return;
    }

    if (newPassword !== confirmNewPassword) {
      notify.error("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await changePassword({
        password,
        new_password: newPassword,
        confirm_new_password: confirmNewPassword,
      });

      if (res?.status === "success") {
        notify.success(
          "Password changed successfully"
        );

        setPassword("");
        setNewPassword("");
        setConfirmNewPassword("");
      } else {
        notify.error(
          res?.message ||
            "Failed to change password"
        );
      }
    } catch (err: any) {
      console.error(err);

      notify.error(
        err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err?.message ||
          "Failed to change password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h1 className="text-2xl font-bold">
        Change Password
      </h1>

      <Input
        type="password"
        placeholder="Current password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <Input
        type="password"
        placeholder="New password"
        value={newPassword}
        onChange={(e) =>
          setNewPassword(e.target.value)
        }
      />

      <Input
        type="password"
        placeholder="Confirm new password"
        value={confirmNewPassword}
        onChange={(e) =>
          setConfirmNewPassword(
            e.target.value
          )
        }
      />

      <Button
        onClick={handleChange}
        disabled={loading}
        className="w-full"
      >
        {loading
          ? "Updating..."
          : "Change Password"}
      </Button>
    </div>
  );
}