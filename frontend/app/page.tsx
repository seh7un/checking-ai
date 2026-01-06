'use client';

import { useState, useEffect } from 'react';
import InstagramUrlInput from '@/components/InstagramUrlInput';
import LoadingSpinner from '@/components/LoadingSpinner';
import InstagramResult from '@/components/InstagramResult';
import GoogleAds from '@/components/GoogleAds';
import { analyzeInstagram, InstagramResult as InstagramResultType } from '@/lib/instagram_api';

export default function Home() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<InstagramResultType | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 환경 변수 확인 (디버깅용)
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    console.log('🌐 Frontend Environment Check:');
    console.log('  - NEXT_PUBLIC_API_URL:', apiUrl);
    console.log('  - Full API URL:', `${apiUrl}/api/instagram/analyze`);
    console.log('  - NODE_ENV:', process.env.NODE_ENV);
  }, []);

  const handleUrlSubmit = async (url: string) => {
    setIsAnalyzing(true);
    setError(null);
    setResult(null);

    try {
      const analysisResult = await analyzeInstagram(url);
      setResult(analysisResult);
    } catch (err: any) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Instagram analysis error:', err.message || 'Unknown error');
      }
      
      const errorMessage = err.message || '인스타그램 게시물 분석 중 오류가 발생했습니다. 다시 시도해주세요.';
      setError(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="mb-4 text-4xl font-bold text-gray-900 dark:text-gray-100 sm:text-5xl">
            인스타그램 크롤러
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-gray-600 dark:text-gray-400">
            인스타그램 게시물 URL을 입력하면 좋아요 수, 댓글 수, 공유 수, 게시 날짜를 분석합니다.
            <br />
            <span className="font-semibold text-blue-600 dark:text-blue-400">
              Instagram의 이용약관을 준수하여 사용해주세요.
            </span>
          </p>
        </header>

        {/* Google Ads */}
        <aside className="mb-6 text-center" aria-label="광고">
          <div className="mx-auto max-w-4xl">
            <GoogleAds 
              slot="1234567890" // 실제 slot ID로 변경 필요
              format="auto"
              className="min-h-[100px]"
            />
          </div>
        </aside>

        {/* Main Content */}
        <div className="mx-auto max-w-4xl">
          {!result && !isAnalyzing && (
            <section aria-label="인스타그램 URL 입력">
              <InstagramUrlInput onUrlSubmit={handleUrlSubmit} isAnalyzing={isAnalyzing} />
            </section>
          )}

          {isAnalyzing && (
            <section aria-label="분석 중">
              <div className="rounded-lg border border-gray-200 bg-white p-8 dark:border-gray-700 dark:bg-gray-800">
                <LoadingSpinner />
              </div>
            </section>
          )}

          {error && (
            <section aria-label="오류 메시지">
              <div className="rounded-lg border border-red-200 bg-red-50 p-6 dark:border-red-900/30 dark:bg-red-900/10">
                <div className="flex items-start">
                  <svg
                    className="mr-3 h-5 w-5 text-red-600 dark:text-red-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <div className="flex-1">
                    <h3 className="font-semibold text-red-900 dark:text-red-200">
                      오류가 발생했습니다
                    </h3>
                    <p className="mt-1 text-sm text-red-700 dark:text-red-300">
                      {error}
                    </p>
                    <button
                      onClick={handleReset}
                      className="mt-4 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-700"
                    >
                      다시 시도
                    </button>
                  </div>
                </div>
              </div>
            </section>
          )}

          {result && (
            <section aria-label="분석 결과">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  분석 결과
                </h2>
                <button
                  onClick={handleReset}
                  className="rounded-lg bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
                >
                  새 게시물 분석
                </button>
              </div>
              <InstagramResult result={result} />
            </section>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>© 2024 인스타그램 크롤러. All rights reserved.</p>
        </footer>
      </div>
    </main>
  );
}
