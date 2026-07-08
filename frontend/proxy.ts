import { NextRequest, NextResponse } from "next/server";

const publicRoutes = [
  "/",
  "/login",
  "/register",
  "/forgot-password",
];

export function proxy(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;

  const role = request.cookies.get("role")?.value;

  const pathname = request.nextUrl.pathname;

  const isPublicRoute = publicRoutes.includes(pathname) || pathname.startsWith("/reset-password");

  if (!token && !isPublicRoute) {
    return NextResponse.redirect(
      new URL("/login", request.url)
    );
  }

  if (token && (pathname === "/login" || pathname === "/register")) {
    return NextResponse.redirect(
      new URL("/profile", request.url)
    );
  }

  if (pathname.startsWith("/admin") && role !== "admin") {
    return NextResponse.redirect(
      new URL("/profile", request.url)
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};