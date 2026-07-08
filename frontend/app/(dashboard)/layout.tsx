"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import LogoutButton from "@/components/auth/logout-button";
import ProtectedRoute from "@/components/auth/protected-route";

const navItems = [
  {
    label: "Documents",
    href: "/documents",
  },
  {
    label: "Search",
    href: "/search",
  },
  {
    label: "Upload",
    href: "/upload",
  },
  {
    label: "Quota",
    href: "/quota",
  },
  {
    label: "Billing",
    href: "/billing",
  },
  {
    label: "Profile",
    href: "/profile",
  },
  {
    label: "Settings",
    href: "/settings",
  },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex">
        <aside className="w-64 border-r p-4 flex flex-col">
          <h1 className="text-xl font-bold text-primary mb-6">
            Tablify
          </h1>

          <nav className="space-y-2 flex-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "block px-3 py-2 rounded-md text-sm transition",
                  pathname === item.href
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          <div className="pt-4 border-t">
            <LogoutButton />
          </div>
        </aside>

        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
}