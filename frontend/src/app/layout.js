import "./globals.css";

import { AntdProvider, QueryProvider } from "@/providers";

export const metadata = {
    title: "URL Shortener",
    description: "A highly scalable URL shortener service",
};

export default function RootLayout({ children }) {
    return (
        <html lang="en" suppressHydrationWarning data-qb-installed="true">
            <body>
                <AntdProvider>
                    <QueryProvider>{children}</QueryProvider>
                </AntdProvider>
            </body>
        </html>
    );
}
