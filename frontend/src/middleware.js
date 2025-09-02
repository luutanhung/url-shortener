import { NextResponse } from "next/server";

export function middleware(req) {
    const token = req.cookies.get("auth-token")?.value;
    const { pathname } = req.nextUrl;

    if (!token && pathname.startsWith("/dashboard")) {
        return NextResponse.redirect(new URL("/auth/login", req.url));
    }

    if (
        token &&
        (pathname.startsWith("/auth/login") ||
            pathname.startsWith("/auth/register"))
    ) {
        return NextResponse.redirect(new URL("/dashboard", req.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ["/dashboard/:path*", "/auth/login", "/auth/register"],
};
