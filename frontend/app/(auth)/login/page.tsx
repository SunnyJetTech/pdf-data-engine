"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useDispatch } from "react-redux";
import { loginUser } from "@/api/auth.api";
import { setUser } from "@/store/slices/authSlice";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { notify } from "@/lib/notify";

export default function LoginPage() {
  const router = useRouter();
  const dispatch = useDispatch();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleLogin() {
    setLoading(true);

    try {
      const res = await loginUser({
        email,
        password,
      });

      if (
        res.status === "success" &&
        res.data
      ) {
        dispatch(
          setUser(res.data.user)
        );

        notify.success(
          "Login successful"
        );

        if (
          res.data.user?.is_admin
        ) {
          router.push("/admin");
        } else {
          router.push("/profile");
        }
      }
    } catch (error) {
      notify.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto space-y-4">
      <h1 className="text-2xl font-bold">
        Login
      </h1>

      <Input
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

      <Button
        className="w-full"
        disabled={loading}
        onClick={handleLogin}
      >
        {loading
          ? "Logging in..."
          : "Login"}
      </Button>

      <div className="flex justify-between text-sm">
        <Link
          href="/register"
          className="text-primary"
        >
          Register
        </Link>

        <Link
          href="/forgot-password"
          className="text-primary"
        >
          Forgot password?
        </Link>
      </div>
    </div>
  );
}