"use client";

import {createContext, useContext, useEffect, useState,} from "react";

type Theme = "light" | "dark";

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({children,}: {children: React.ReactNode;}) {
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const saved = (localStorage.getItem("theme") as Theme) || "light";

    setTheme(saved);

    document.documentElement.classList.remove("light", "dark");

    document.documentElement.classList.add(saved);
  }, []);

  function toggleTheme() {
    const newTheme =
      theme === "light"
        ? "dark"
        : "light";

    setTheme(newTheme);

    localStorage.setItem("theme", newTheme);

    document.documentElement.classList.remove(
      "light",
      "dark"
    );

    document.documentElement.classList.add(newTheme);
  }

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error(
      "useTheme must be used inside ThemeProvider"
    );
  }

  return context;
}