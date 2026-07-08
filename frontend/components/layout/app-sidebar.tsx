"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  User,
  Upload,
  FileText,
  Search,
  Settings,
} from "lucide-react";

const items = [
  {label: "Profile", href: "/profile", icon: User,},
  {label: "Upload PDF", href: "/upload", icon: Upload,},
  {label: "Documents", href: "/documents", icon: FileText,},
  {label: "Search", href: "/search", icon: Search,},
  {label: "Settings", href: "/settings", icon: Settings,},
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 min-h-screen bg-[#0B1F3A] border-r border-[#1F2937] p-5">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-white">
          Tablify
        </h1>

        <p className="text-xs text-gray-400">
          PDF → Data Engine
        </p>
      </div>

      <nav className="space-y-2">
        {items.map((item) => {
          const Icon = item.icon;

          const active =
            pathname === item.href ||
            pathname.startsWith(`${item.href}/`);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-md transition-colors ${
                active
                  ? "bg-blue-700 text-white"
                  : "text-gray-300 hover:bg-[#111827] hover:text-white"
              }`}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}