"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "@/providers/theme-provider";

export default function ThemeToggle() {
  const {theme, toggleTheme,} = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="
        flex items-center gap-2
        rounded-md border
        px-3 py-2
        text-sm
      "
    >
      {theme === "dark" ? (
        <>
          <Sun size={16} />
        </>
      ) : (
        <>
          <Moon size={16} />
        </>
      )}
    </button>
  );
}