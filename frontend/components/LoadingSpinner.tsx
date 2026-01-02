'use client';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="relative">
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-solid border-blue-200 border-t-blue-600"></div>
      </div>
      <p className="mt-4 text-lg font-medium text-gray-700 dark:text-gray-300">
        문서를 분석하는 중...
      </p>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
        잠시만 기다려주세요
      </p>
    </div>
  );
}

