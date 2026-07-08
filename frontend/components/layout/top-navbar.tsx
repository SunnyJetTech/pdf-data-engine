"use client"

import { Input } from "@/components/ui/input"
import { Bell, User } from "lucide-react"

export function Topbar() {
  return (
    <header className="h-16 border-b border-[#1F2937] bg-[#0A0F1C] px-6 flex items-center justify-between">
      <div className="w-1/3">
        <Input
          placeholder="Search documents..."
          className="bg-[#111827] border-[#1F2937] text-white"
        />
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-md hover:bg-[#111827]">
          <Bell size={18} />
        </button>

        <button className="flex items-center gap-2 px-3 py-1 rounded-md bg-[#111827]">
          <User size={18} />
          <span className="text-sm">Account</span>
        </button>
      </div>
    </header>
  )
}