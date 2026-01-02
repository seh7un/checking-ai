'use client';

import { useEffect } from 'react';

interface GoogleAdsProps {
  slot: string;
  format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal';
  style?: React.CSSProperties;
  className?: string;
}

/**
 * Google AdSense 광고 컴포넌트
 * 
 * 사용 방법:
 * 1. Google AdSense 계정 생성 및 승인
 * 2. 광고 단위 생성 후 publisher-id와 slot-id 확인
 * 3. 환경 변수에 NEXT_PUBLIC_GOOGLE_ADSENSE_ID 설정
 * 4. 이 컴포넌트에 slot prop 전달
 */
export default function GoogleAds({ 
  slot, 
  format = 'auto',
  style,
  className = ''
}: GoogleAdsProps) {
  const publisherId = process.env.NEXT_PUBLIC_GOOGLE_ADSENSE_ID;

  useEffect(() => {
    // Google AdSense 스크립트 로드
    if (typeof window !== 'undefined' && publisherId) {
      // 이미 로드되었는지 확인
      if (!document.querySelector(`script[src*="adsbygoogle"]`)) {
        const script = document.createElement('script');
        script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${publisherId}`;
        script.async = true;
        script.crossOrigin = 'anonymous';
        document.head.appendChild(script);
      }

      // 광고 초기화
      try {
        ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({});
      } catch (e) {
        console.error('Google Ads initialization error:', e);
      }
    }
  }, [publisherId]);

  // Publisher ID가 없으면 플레이스홀더 표시
  if (!publisherId) {
    return (
      <div 
        className={`flex items-center justify-center border-2 border-dashed border-gray-300 bg-gray-50 p-8 dark:border-gray-700 dark:bg-gray-800/50 ${className}`}
        style={style}
      >
        <div className="text-center">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
            Google Ads 영역
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-500">
            Google AdSense 설정이 필요합니다
          </p>
          <p className="text-xs text-gray-400 dark:text-gray-600 mt-1">
            NEXT_PUBLIC_GOOGLE_ADSENSE_ID 환경 변수를 설정하세요
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={className} style={style}>
      <ins
        className="adsbygoogle"
        style={{
          display: 'block',
          ...style,
        }}
        data-ad-client={publisherId}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}

