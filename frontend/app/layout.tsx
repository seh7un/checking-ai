import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "인스타그램 크롤러",
  description: "인스타그램 게시물 URL을 입력하면 좋아요 수, 댓글 수, 공유 수, 게시 날짜를 분석하는 서비스.",
  keywords: ["인스타그램", "크롤링", "좋아요", "댓글", "인스타그램 분석", "SNS 분석"],
  authors: [{ name: "인스타그램 크롤러" }],
  openGraph: {
    title: "인스타그램 크롤러",
    description: "인스타그램 게시물의 좋아요, 댓글, 공유 수를 분석합니다.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#ffffff" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
