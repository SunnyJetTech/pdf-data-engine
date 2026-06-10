import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/auth-context"

export const metadata: Metadata = {
  title: "E-Commerce Application",
  description: "For all cosmetic products",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={` h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
