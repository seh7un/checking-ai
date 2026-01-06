'use client';

import { InstagramResult as InstagramResultType } from '@/lib/instagram_api';

interface InstagramResultProps {
  result: InstagramResultType;
}

export default function InstagramResult({ result }: InstagramResultProps) {
  const { data } = result;

  const formatNumber = (num: number | null) => {
    if (num === null || num === undefined) return 'N/A';
    return num.toLocaleString('ko-KR');
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'N/A';
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="space-y-6">
      {/* 기본 정보 */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h3 className="mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
          게시물 정보
        </h3>
        <div className="space-y-3">
          <div>
            <span className="text-sm font-medium text-gray-500 dark:text-gray-400">URL:</span>
            <a
              href={data.url}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 text-blue-600 hover:underline dark:text-blue-400"
            >
              {data.url}
            </a>
          </div>
          {data.username && (
            <div>
              <span className="text-sm font-medium text-gray-500 dark:text-gray-400">사용자:</span>
              <span className="ml-2 text-gray-900 dark:text-gray-100">@{data.username}</span>
            </div>
          )}
          {data.post_id && (
            <div>
              <span className="text-sm font-medium text-gray-500 dark:text-gray-400">게시물 ID:</span>
              <span className="ml-2 text-gray-900 dark:text-gray-100">{data.post_id}</span>
            </div>
          )}
        </div>
      </div>

      {/* 통계 */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {/* 좋아요 */}
        <div className="rounded-lg border border-gray-200 bg-gradient-to-br from-pink-50 to-pink-100 p-6 dark:border-gray-700 dark:from-pink-900/20 dark:to-pink-800/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">좋아요</p>
              <p className="mt-1 text-2xl font-bold text-gray-900 dark:text-gray-100">
                {formatNumber(data.like_count)}
              </p>
            </div>
            <div className="rounded-full bg-pink-200 p-3 dark:bg-pink-800/30">
              <svg
                className="h-6 w-6 text-pink-600 dark:text-pink-400"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* 댓글 */}
        <div className="rounded-lg border border-gray-200 bg-gradient-to-br from-blue-50 to-blue-100 p-6 dark:border-gray-700 dark:from-blue-900/20 dark:to-blue-800/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">댓글</p>
              <p className="mt-1 text-2xl font-bold text-gray-900 dark:text-gray-100">
                {formatNumber(data.comment_count)}
              </p>
            </div>
            <div className="rounded-full bg-blue-200 p-3 dark:bg-blue-800/30">
              <svg
                className="h-6 w-6 text-blue-600 dark:text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* 공유 */}
        <div className="rounded-lg border border-gray-200 bg-gradient-to-br from-green-50 to-green-100 p-6 dark:border-gray-700 dark:from-green-900/20 dark:to-green-800/20">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">공유</p>
              <p className="mt-1 text-2xl font-bold text-gray-900 dark:text-gray-100">
                {formatNumber(data.share_count)}
              </p>
            </div>
            <div className="rounded-full bg-green-200 p-3 dark:bg-green-800/30">
              <svg
                className="h-6 w-6 text-green-600 dark:text-green-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8.684 13.342C8.885 12.938 9 12.482 9 12c0-.482-.115-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* 날짜 */}
      {data.post_date && (
        <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
          <h3 className="mb-2 text-sm font-medium text-gray-500 dark:text-gray-400">게시 날짜</h3>
          <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            {formatDate(data.post_date)}
          </p>
        </div>
      )}

      {/* 캡션 */}
      {data.caption && (
        <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
          <h3 className="mb-2 text-sm font-medium text-gray-500 dark:text-gray-400">캡션</h3>
          <p className="text-gray-900 dark:text-gray-100">{data.caption}</p>
        </div>
      )}

      {/* 안내 */}
      <div className="rounded-lg border-2 border-yellow-300 bg-yellow-50 p-4 dark:border-yellow-700 dark:bg-yellow-900/20">
        <div className="flex items-start gap-3">
          <svg
            className="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-600 dark:text-yellow-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div className="flex-1">
            <h3 className="mb-1 font-semibold text-yellow-900 dark:text-yellow-200">안내</h3>
            <p className="text-sm leading-relaxed text-yellow-800 dark:text-yellow-300">
              Instagram은 공유 수를 직접 제공하지 않을 수 있습니다. 
              비공개 계정의 게시물은 크롤링할 수 없으며, Instagram의 이용약관을 준수해야 합니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

