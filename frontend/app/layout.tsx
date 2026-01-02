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
  title: "계약 문서 분석기",
  description: "계약서에서 개인정보 노출, 불리한 조항, 법적 위험 요소를 자동으로 분석하는 서비스. Zero Storage 정책으로 모든 파일은 메모리에서만 처리됩니다.",
  keywords: ["계약서 분석", "계약 문서", "법적 위험", "개인정보 보호", "계약 검토", "문서 분석"],
  authors: [{ name: "계약 문서 분석기" }],
  openGraph: {
    title: "계약 문서 분석기",
    description: "계약서에서 개인정보 노출과 법적 위험 요소를 자동으로 분석합니다.",
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
