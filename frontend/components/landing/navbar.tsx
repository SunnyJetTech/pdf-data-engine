"use client";

import Link from "next/link";
import Container from "@/components/layout/container";
import ThemeToggle from "@/components/theme-toggle";
import LogoutButton from "@/components/auth/logout-button";
import { Button } from "@/components/ui/button";
import { useAppSelector } from "@/store/hooks";

export default function Navbar() {
  const user = useAppSelector(
    (state) => state.auth.user
  );

  const loading = useAppSelector(
    (state) => state.auth.loading
  );

  return (
    <header className="border-b sticky top-0 z-50 bg-background/95 backdrop-blur">
      <Container>
        <div className="h-16 flex items-center justify-between">
          <Link
            href="/"
            className="font-bold text-2xl text-primary"
          >
            Tablify
          </Link>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            {!loading && (
              user ? (
                <>
                  <Link href="/">
                    <Button variant="outline">
                      Home
                    </Button>
                  </Link>

                  <Link href="/profile">
                    <Button variant="outline">
                      Profile
                    </Button>
                  </Link>

                  {user.is_admin && (
                    <Link href="/admin">
                      <Button variant="outline">
                        Admin
                      </Button>
                    </Link>
                  )}

                  <LogoutButton />
                </>
              ) : (
                <>
                  <Link href="/login">
                    <Button variant="outline">
                      Login
                    </Button>
                  </Link>

                  <Link href="/register">
                    <Button>
                      Get Started
                    </Button>
                  </Link>
                </>
              )
            )}
          </div>
        </div>
      </Container>
    </header>
  );
}