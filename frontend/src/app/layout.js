import "./globals.css";

import QueryProvider from "@/providers/queryProvider";

export const metadata = {
  title: "URL Shortener",
  description: "A highly scalable URL shortener service",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
