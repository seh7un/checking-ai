'use client';

import { useState, useEffect } from 'react';
import FileUpload from '@/components/FileUpload';
import LoadingSpinner from '@/components/LoadingSpinner';
import AnalysisResult from '@/components/AnalysisResult';
import GoogleAds from '@/components/GoogleAds';
import { analyzeDocument, AnalysisResult as AnalysisResultType } from '@/lib/api';

export default function Home() {
  const [isUploading, setIsUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResultType | null>(null);
  const [error, setError] = useState<string | null>(null);

  // 환경 변수 확인 (디버깅용)
  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    console.log('🌐 Frontend Environment Check:');
    console.log('  - NEXT_PUBLIC_API_URL:', apiUrl);
    console.log('  - Full API URL:', `${apiUrl}/api/analyze`);
    console.log('  - NODE_ENV:', process.env.NODE_ENV);
  }, []);

  const handleFileSelect = async (file: File) => {
    setIsUploading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await analyzeDocument(file);
      setAnalysisResult(result);
    } catch (err: any) {
      // 에러 로깅 (민감 정보 제외)
      // console.error는 개발 환경에서만 사용
      if (process.env.NODE_ENV === 'development') {
        console.error('Analysis error:', err.message || 'Unknown error');
      }
      
      // 사용자에게 안전한 에러 메시지 표시
      const errorMessage = err.message || '문서 분석 중 오류가 발생했습니다. 다시 시도해주세요.';
      setError(errorMessage);
    } finally {
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Header */}
        <header className="mb-8 text-center">
          <h1 className="mb-4 text-4xl font-bold text-gray-900 dark:text-gray-100 sm:text-5xl">
            계약 문서 분석기
          </h1>
          <p className="mx-auto max-w-2xl text-lg text-gray-600 dark:text-gray-400">
            계약서에서 개인정보 노출, 불리한 조항, 법적 위험 요소를 자동으로 분석합니다.
            <br />
            <span className="font-semibold text-blue-600 dark:text-blue-400">
              모든 파일은 메모리에서만 처리되며 서버에 저장되지 않습니다.
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
          {!analysisResult && !isUploading && (
            <section aria-label="파일 업로드">
              <FileUpload onFileSelect={handleFileSelect} isUploading={isUploading} />
            </section>
          )}

          {isUploading && (
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

          {analysisResult && (
            <section aria-label="분석 결과">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  분석 결과
                </h2>
                <button
                  onClick={handleReset}
                  className="rounded-lg bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
                >
                  새 문서 분석
                </button>
              </div>
              <AnalysisResult result={analysisResult} />
            </section>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500 dark:text-gray-400">
          <p>© 2024 계약 문서 분석기. All rights reserved.</p>
        </footer>
      </div>
    </main>
  );
}
