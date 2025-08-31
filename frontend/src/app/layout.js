import "./globals.css";

export const metadata = {
  title: "URL Shortener",
  description: "A highly scalable URL shortener service",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
