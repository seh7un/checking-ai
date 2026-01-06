'use client';

import { useState } from 'react';

interface InstagramUrlInputProps {
  onUrlSubmit: (url: string) => void;
  isAnalyzing: boolean;
}

export default function InstagramUrlInput({ onUrlSubmit, isAnalyzing }: InstagramUrlInputProps) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!url.trim()) {
      setError('인스타그램 URL을 입력해주세요.');
      return;
    }

    if (!url.includes('instagram.com')) {
      setError('올바른 인스타그램 URL을 입력해주세요.');
      return;
    }

    onUrlSubmit(url.trim());
  };

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-8 dark:border-gray-700 dark:bg-gray-800">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="instagram-url" className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
            인스타그램 게시물 URL
          </label>
          <input
            id="instagram-url"
            type="url"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setError(null);
            }}
            placeholder="https://www.instagram.com/p/ABC123/"
            disabled={isAnalyzing}
            className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 dark:placeholder-gray-400"
          />
          {error && (
            <p className="mt-2 text-sm text-red-600 dark:text-red-400">{error}</p>
          )}
          <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            예: https://www.instagram.com/p/ABC123/ 또는 https://www.instagram.com/reel/ABC123/
          </p>
        </div>
        <button
          type="submit"
          disabled={isAnalyzing}
          className="w-full rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-blue-500 dark:hover:bg-blue-600"
        >
          {isAnalyzing ? '분석 중...' : '분석하기'}
        </button>
      </form>
    </div>
  );
}

