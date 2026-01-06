# 인스타그램 크롤링 사이트 개발 계획

## 프로젝트 개요

**목표:** 인스타그램 게시물 URL을 입력받아 좋아요 수, 댓글 수, 공유 수, 날짜를 크롤링하는 웹 서비스

## 기능 명세

### 입력
- 인스타그램 게시물 URL (예: `https://www.instagram.com/p/ABC123/`)

### 출력
- 좋아요 수 (Like Count)
- 댓글 수 (Comment Count)
- 공유 수 (Share Count) - Instagram은 공유 수를 직접 제공하지 않을 수 있음
- 게시 날짜 (Post Date)

## 기술 스택

### 백엔드
- **FastAPI** (기존 구조 유지)
- **크롤링 라이브러리 옵션:**
  1. **instaloader** (Python 라이브러리, 비공식)
  2. **requests + BeautifulSoup** (웹 스크래핑)
  3. **Instagram Graph API** (공식 API, 제한적)
  4. **selenium** (브라우저 자동화, 느림)

### 프론트엔드
- **Next.js 14+** (기존 구조 유지)
- **Tailwind CSS** (기존 구조 유지)
- **TypeScript** (기존 구조 유지)

## 구현 계획

### Phase 1: 백엔드 크롤링 로직
1. 크롤링 라이브러리 선택 및 설치
2. Instagram URL 파싱 및 검증
3. 게시물 정보 추출 (좋아요, 댓글, 날짜)
4. API 엔드포인트 구현

### Phase 2: 프론트엔드 UI
1. URL 입력 폼
2. 로딩 상태 표시
3. 결과 표시 컴포넌트
4. 에러 처리

### Phase 3: 배포 및 최적화
1. 에러 처리 개선
2. 이용약관 준수 안내
3. 배포

## 주의사항

### Instagram 이용약관
- Instagram은 공식적으로 웹 스크래핑을 금지할 수 있음
- 공식 API 사용 권장 (Instagram Graph API)
- 비공식 크롤링은 법적 문제 가능성

### 대안
1. **Instagram Graph API 사용** (공식, 제한적)
2. **사용자에게 Instagram API 토큰 입력 요청**
3. **이용약관 준수 안내 표시**

## API 설계

### 엔드포인트
```
POST /api/instagram/analyze
```

### 요청
```json
{
  "url": "https://www.instagram.com/p/ABC123/"
}
```

### 응답
```json
{
  "status": "success",
  "data": {
    "url": "https://www.instagram.com/p/ABC123/",
    "like_count": 1234,
    "comment_count": 56,
    "share_count": null,  // Instagram은 공유 수를 직접 제공하지 않을 수 있음
    "post_date": "2024-01-15T10:30:00Z",
    "caption": "게시물 설명...",
    "username": "username"
  }
}
```

## 파일 구조

```
backend/
├── main.py (기존 유지, 새 엔드포인트 추가)
├── utils/
│   ├── instagram_crawler.py (새 파일)
│   └── ...
└── requirements.txt (크롤링 라이브러리 추가)

frontend/
├── app/
│   ├── page.tsx (기존 교체 또는 새 페이지)
│   └── ...
└── components/
    ├── InstagramUrlInput.tsx (새 컴포넌트)
    └── InstagramResult.tsx (새 컴포넌트)
```

## 다음 단계

1. 크롤링 라이브러리 선택 및 테스트
2. 백엔드 크롤링 로직 구현
3. 프론트엔드 UI 구현
4. 통합 테스트

