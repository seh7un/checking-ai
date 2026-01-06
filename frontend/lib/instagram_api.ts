/**
 * 인스타그램 크롤링 API 통신 유틸리티
 */
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface InstagramResult {
  status: string;
  message: string;
  data: {
    url: string;
    post_id: string | null;
    username: string | null;
    like_count: number | null;
    comment_count: number | null;
    share_count: number | null;
    post_date: string | null;
    caption: string | null;
  };
}

export const analyzeInstagram = async (url: string): Promise<InstagramResult> => {
  // URL 검증
  if (!url) {
    throw new Error('인스타그램 URL을 입력해주세요.');
  }

  if (!url.includes('instagram.com')) {
    throw new Error('올바른 인스타그램 URL을 입력해주세요.');
  }

  try {
    const response = await axios.post<InstagramResult>(
      `${API_BASE_URL}/api/instagram/analyze`,
      { url },
      {
        timeout: 30000, // 30초 타임아웃
      }
    );

    return response.data;
  } catch (error: any) {
    // 에러 처리
    if (error.response) {
      const errorMessage = error.response.data?.detail || error.response.data?.message || '서버 오류가 발생했습니다.';
      throw new Error(errorMessage);
    } else if (error.request) {
      throw new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.');
    } else {
      throw new Error('요청 처리 중 오류가 발생했습니다.');
    }
  }
};

