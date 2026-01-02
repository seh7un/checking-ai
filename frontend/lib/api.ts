/**
 * API 통신 유틸리티
 * 백엔드 FastAPI 서버와 통신
 */
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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

  try {
    // API URL 확인 (디버깅용)
    if (process.env.NODE_ENV === 'development') {
      console.log('API Base URL:', API_BASE_URL);
      console.log('Full URL:', `${API_BASE_URL}/api/analyze`);
    }

    const response = await axios.post<AnalysisResult>(
      `${API_BASE_URL}/api/analyze`,
      formData,
      {
        // FormData를 사용할 때는 headers를 아예 설정하지 않아야 함
        // 브라우저가 자동으로 boundary를 포함한 Content-Type을 설정함
        timeout: 60000, // 60초 타임아웃
        // withCredentials: false, // CORS 문제 시 필요할 수 있음
      }
    );

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

