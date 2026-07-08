"use client"

import Link from "next/link"
import { useSelector } from "react-redux"
import { RootState } from "@/store"
import LogoutButton from "@/components/auth/logout-button"

export default function Navbar() {
  const user = useSelector(
      (state: RootState) =>
    state.auth.user
    )

  return (
    <header className="border-b">
      <div className="container mx-auto h-16 flex items-center justify-between">
        <Link
          href="/"
          className="font-bold text-xl"
        >
          Tablify
        </Link>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link href="/profile">
                Profile
              </Link>

              {user.is_admin && (
                <Link href="/admin">
                  Admin
                </Link>
              )}

              <LogoutButton />
            </>
          ) : (
            <>
              <Link href="/login">
                Login
              </Link>

              <Link href="/register">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}