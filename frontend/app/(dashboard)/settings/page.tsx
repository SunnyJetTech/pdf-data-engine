"use client";

import { useState } from "react";
import { changePassword } from "@/api/auth.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner"


export default function SettingsPage() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword,] = useState("");
  const [loading, setLoading] = useState(false);

  async function submitForm() {
    if (!currentPassword.trim() || !newPassword.trim() || !confirmNewPassword.trim()) {
      toast.error("All fields are required");
      return;
    }

    if (newPassword !== confirmNewPassword) {
      toast.error("Passwords do not match");
      return;
    }

    if (newPassword.length < 6) {
      toast.error("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      const response = await changePassword({
          password: currentPassword,
          new_password: newPassword,
          confirm_new_password: confirmNewPassword,
        });

      if (response?.status === "success") {
        toast.success(response.message || "Password changed successfully");

        setCurrentPassword("");
        setNewPassword("");
        setConfirmNewPassword("");
      } else {
        toast.error(response?.message || "Failed to update password");
      }
    } catch (error: any) {
      toast.error(
        error?.response?.data
          ?.message ||
          error?.response?.data
            ?.detail ||
          "Failed to update password"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-lg space-y-6">
      <h1 className="text-3xl font-bold">
        Settings
      </h1>

      <div className="border rounded-lg p-6 space-y-4">
        <h2 className="font-semibold">
          Change Password
        </h2>

        <Input
          type="password"
          placeholder="Current Password"
          value={currentPassword}
          onChange={(e) =>
            setCurrentPassword(
              e.target.value
            )
          }
        />

        <Input
          type="password"
          placeholder="New Password"
          value={newPassword}
          onChange={(e) =>
            setNewPassword(
              e.target.value
            )
          }
        />

        <Input
          type="password"
          placeholder="Confirm New Password"
          value={
            confirmNewPassword
          }
          onChange={(e) =>
            setConfirmNewPassword(
              e.target.value
            )
          }
        />

        <Button
          onClick={submitForm}
          disabled={loading}
          className="w-full"
        >
          {loading
            ? "Updating..."
            : "Update Password"}
        </Button>
      </div>
    </div>
  );
}