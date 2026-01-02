/**
 * API 통신 유틸리티
 * 백엔드 FastAPI 서버와 통신
 */
import axios from 'axios';

// 환경 변수는 빌드 타임에 정적으로 대체됨
// 브라우저에서는 process.env를 직접 접근할 수 없음
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 프로토콜이 없는 경우 자동으로 추가 (호환성)
if (API_BASE_URL && !API_BASE_URL.startsWith('http://') && !API_BASE_URL.startsWith('https://')) {
  API_BASE_URL = `https://${API_BASE_URL}`;
  console.warn('⚠️ API URL에 프로토콜이 없어서 https://를 자동 추가했습니다. Vercel 환경 변수를 수정하세요.');
}

// 전역 변수로 노출 (디버깅용)
if (typeof window !== 'undefined') {
  (window as any).__API_BASE_URL__ = API_BASE_URL;
  console.log('🔧 API Base URL (from build):', API_BASE_URL);
}

export interface AnalysisResult {
  status: string;
  message: string;
  file_info: {
    filename: string;
    content_type: string;
    size_bytes: number;
  };
  analysis: {
    risk_level: 'high' | 'medium' | 'low';
    pii_analysis: {
      findings: Array<{
        type: string;
        value: string;
        severity: 'high' | 'medium' | 'low';
        position: [number, number];
        description: string;
      }>;
      summary: {
        total_count: number;
        high_severity: number;
        medium_severity: number;
        low_severity: number;
      };
    };
    ai_analysis: {
      method: 'openai' | 'mock';
      note?: string;
      result: {
        risk_level: 'high' | 'medium' | 'low';
        issues: Array<{
          type: string;
          severity: 'high' | 'medium' | 'low';
          description: string;
          problematic_text?: string;
          corrected_text?: string;
          suggestion: string;
        }>;
        summary: string;
      };
    };
    storage_policy: string;
    disclaimer?: string;
  };
}

export const analyzeDocument = async (file: File): Promise<AnalysisResult> => {
  // 파일 검증
  if (!file) {
    throw new Error('파일이 선택되지 않았습니다.');
  }

  // 파일 크기 검증 (10MB)
  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    throw new Error(`파일 크기가 너무 큽니다. 최대 ${maxSize / (1024 * 1024)}MB까지 업로드 가능합니다.`);
  }

  // 파일 타입 검증
  const allowedTypes = [
    'application/pdf',
    'text/plain',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ];
  if (!allowedTypes.includes(file.type)) {
    throw new Error('지원하지 않는 파일 형식입니다. PDF, TXT, DOCX 파일만 업로드 가능합니다.');
  }

  const formData = new FormData();
  formData.append('file', file);

  // API URL 확인 (항상 로그 출력)
  const fullUrl = `${API_BASE_URL}/api/analyze`;
  console.log('🔍 API Request Debug:');
  console.log('  - API Base URL:', API_BASE_URL);
  console.log('  - Full URL:', fullUrl);
  console.log('  - File name:', file.name);
  console.log('  - File size:', file.size);
  console.log('  - File type:', file.type);

  try {
    const response = await axios.post<AnalysisResult>(
      fullUrl,
      formData,
      {
        // FormData를 사용할 때는 headers를 아예 설정하지 않아야 함
        // 브라우저가 자동으로 boundary를 포함한 Content-Type을 설정함
        timeout: 60000, // 60초 타임아웃
        // CORS 관련 설정
        withCredentials: false,
        // 요청 인터셉터로 실제 요청 확인
        transformRequest: [(data) => {
          console.log('📤 Sending request to:', fullUrl);
          return data;
        }],
      }
    );

    console.log('✅ Response received:', response.status);
    return response.data;
  } catch (error: any) {
    // 에러 처리 (민감 정보 노출 방지)
    if (error.response) {
      // 서버 응답이 있는 경우
      const errorMessage = error.response.data?.detail || error.response.data?.message || '서버 오류가 발생했습니다.';
      throw new Error(errorMessage);
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못한 경우
      throw new Error('서버에 연결할 수 없습니다. 네트워크 연결을 확인해주세요.');
    } else {
      // 요청 설정 중 오류
      throw new Error('요청 처리 중 오류가 발생했습니다.');
    }
  }
};

