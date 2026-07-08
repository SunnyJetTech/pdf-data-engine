import type { Metadata } from "next";
import "./globals.css";
import { JetBrains_Mono } from "next/font/google";
import { cn } from "@/lib/utils";
import QueryProvider from "@/providers/query-provider";
import { Toaster } from "sonner";
import ReduxProvider from "./providers";
import { ThemeProvider } from "@/providers/theme-provider";
import AuthHydrator from "@/components/auth/auth-hydrator"

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Tablify",
  description:
    "Upload PDFs, convert them into structured data, and search instantly.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn(
        "h-full",
        "antialiased",
        "font-mono",
        jetbrainsMono.variable
      )}

      suppressHydrationWarning
    >
      <body className="min-h-full">
        <ReduxProvider>
          <AuthHydrator />

          <QueryProvider>
            <ThemeProvider>
              {children}
              <Toaster richColors position="top-right"/>
            </ThemeProvider>
          </QueryProvider>
        </ReduxProvider>
      </body>
    </html>
  );
}