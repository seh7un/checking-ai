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
  title: "민감 문서 분석기 - Stateless Document Analyzer",
  description: "개인정보와 법적 위험 요소를 자동으로 분석하는 보안 문서 분석 서비스. Zero Storage 정책으로 모든 파일은 메모리에서만 처리됩니다.",
  keywords: ["문서 분석", "개인정보 보호", "PII 감지", "문서 보안", "민감 정보 분석"],
  authors: [{ name: "Stateless Document Analyzer" }],
  openGraph: {
    title: "민감 문서 분석기",
    description: "업로드한 문서에서 개인정보와 법적 위험 요소를 자동으로 분석합니다.",
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
