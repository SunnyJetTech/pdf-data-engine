"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { registerUser } from "@/api/auth.api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getErrorMessage } from "@/lib/utils/errorHandler";
import { notify } from "@/lib/notify";

export default function RegisterPage() {
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] =
    useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleRegister() {
    setError("");

    if (
      !username ||
      !email ||
      !password ||
      !confirmPassword
    ) {
      setError("All fields are required");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);

    try {
      const res = await registerUser({
        username,
        email,
        password,
        confirm_password: confirmPassword,
      });

      if (res.status === "success") {
        notify.success(res.message)

        setTimeout(() => {
          router.push("/login");
        }, 300);
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h1 className="text-3xl font-bold">
        Create Account
      </h1>

      {error && (
        <div className="rounded border border-red-500 p-3 text-red-500">
          {error}
        </div>
      )}

      <Input
        placeholder="Username"
        value={username}
        onChange={(e) =>
          setUsername(e.target.value)
        }
      />

      <Input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) =>
          setEmail(e.target.value)
        }
      />

      <Input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) =>
          setPassword(e.target.value)
        }
      />

      <Input
        type="password"
        placeholder="Confirm Password"
        value={confirmPassword}
        onChange={(e) =>
          setConfirmPassword(e.target.value)
        }
      />

      <Button
        className="w-full"
        onClick={handleRegister}
        disabled={loading}
      >
        {loading
          ? "Creating Account..."
          : "Register"}
      </Button>

      <div className="flex justify-between text-sm">
        <Link
          href="/login"
          className="text-blue-500 hover:underline"
        >
          Login
        </Link>

        <Link
          href="/forgot-password"
          className="text-blue-500 hover:underline"
        >
          Forgot Password?
        </Link>
      </div>
    </div>
  );
}