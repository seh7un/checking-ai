# Stateless Sensitive Document Analyzer (MVP)

보안과 심층 분석을 핵심 가치로 하는 문서 분석 웹 서비스

## 핵심 원칙

- **Zero Storage Policy:** 업로드된 문서는 절대 서버 디스크나 DB에 저장되지 않음
- **Memory Only:** 모든 파일 처리는 RAM에서만 이루어지며, 분석 완료 후 즉시 휘발

## Tech Stack

- **Frontend:** Next.js 14+ (App Router), Tailwind CSS, TypeScript
- **Backend:** FastAPI (Python)
- **Analysis:** PII 감지 + LLM 기반 민감도 분석

## 프로젝트 구조

```
.
├── backend/              # FastAPI 백엔드
│   ├── main.py          # FastAPI 애플리케이션
│   ├── requirements.txt # Python 의존성
│   ├── .env             # 환경 변수 (API Key 등)
│   └── utils/           # 분석 유틸리티 모듈
│       ├── __init__.py
│       ├── text_extractor.py  # 텍스트 추출 (PDF, TXT, DOCX)
│       ├── pii_detector.py    # PII 감지 (정규식 기반)
│       ├── ai_analyzer.py     # AI 기반 문맥 분석
│       └── logger.py          # 안전한 로깅 유틸리티
└── frontend/            # Next.js 프론트엔드
    ├── app/             # App Router
    │   ├── layout.tsx   # 루트 레이아웃 (SEO 최적화)
    │   └── page.tsx     # 메인 페이지
    ├── components/      # React 컴포넌트
    │   ├── FileUpload.tsx      # 파일 업로드 컴포넌트
    │   ├── LoadingSpinner.tsx  # 로딩 스피너
    │   └── AnalysisResult.tsx  # 분석 결과 표시
    └── lib/             # 유틸리티
        └── api.ts       # API 통신 로직
```

## 개발 가이드

### Backend 실행

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

API는 `http://localhost:8000`에서 실행됩니다.

### Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

### API 엔드포인트

- `GET /`: Health check
- `POST /api/analyze`: 문서 업로드 및 분석 (메모리 기반)
  - 지원 형식: PDF, TXT, DOCX
  - 1차 분석: PII 감지 (전화번호, 주민번호, 이메일, 신용카드 등)
  - 2차 분석: AI 기반 문맥 분석 (OpenAI API 또는 Mock)

### 환경 변수 설정 (선택사항)

OpenAI API를 사용하려면 `.env` 파일을 생성하세요:

**방법 1: .env 파일 사용 (권장)**

```bash
cd backend
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 열어서 실제 API Key 입력
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

**방법 2: 환경 변수로 직접 설정**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

> **참고:** API Key가 없어도 Mock 분석이 자동으로 수행됩니다. 실제 OpenAI API를 사용하려면 [OpenAI Platform](https://platform.openai.com/api-keys)에서 API Key를 발급받으세요.

## 분석 기능

### 1차 분석 (Rule-based PII Detection)
- 한국 휴대폰 번호 감지
- 주민등록번호 패턴 감지
- 이메일 주소 감지
- 신용카드 번호 패턴 감지

### 2차 분석 (AI-based Context Analysis)
- 공격적/비방 표현 감지
- 법적 위험 요소 분석
- 비밀 유지 위반 가능성 검토
- 개인정보 노출 위험 평가

## 보안 기능

### 에러 핸들링
- 전역 예외 핸들러로 모든 예외 안전하게 처리
- 클라이언트에는 일반적인 에러 메시지만 반환
- 상세한 에러 정보는 서버 로그에만 기록

### 민감 정보 보호
- 로그에서 개인정보 자동 마스킹
- API Key는 로그에 노출되지 않음
- 에러 메시지에 민감 정보 포함 방지

### 입력 검증
- 파일 크기 제한 (10MB)
- 파일 타입 검증
- 위험한 파일명 차단
- 빈 파일 거부

자세한 내용은 [SECURITY.md](./SECURITY.md)를 참조하세요.

## 배포

실제 URL로 서비스를 배포하는 방법은 [DEPLOYMENT.md](./DEPLOYMENT.md)를 참조하세요.

**빠른 체크리스트:** [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

## 진행 상황

- [x] Step 1: Project Setup & Backend Skeleton
- [x] Step 2: Analysis Logic Implementation
- [x] Step 3: Frontend Implementation
- [x] Step 4: Safety & Cleanup
- [x] Google Ads 통합

