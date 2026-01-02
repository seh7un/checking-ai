# 405 에러 해결 가이드

## 문제
```
Failed to load resource: the server responded with a status of 405
```

## 원인
405 에러는 "Method Not Allowed"를 의미합니다. 

**주요 원인:**
- FormData를 사용할 때 `Content-Type: multipart/form-data`를 명시적으로 설정하면, 브라우저가 boundary를 포함한 올바른 Content-Type을 자동으로 설정하지 못함
- 이로 인해 서버가 요청을 올바르게 파싱하지 못하고 405 에러 발생

## 해결 방법

### ✅ 수정 완료
`frontend/lib/api.ts`에서 `Content-Type` 헤더를 제거했습니다.

**수정 전:**
```typescript
headers: {
  'Content-Type': 'multipart/form-data',
}
```

**수정 후:**
```typescript
headers: {
  // 'Content-Type' 제거 - FormData가 자동으로 설정함
}
```

## 다음 단계

1. **Vercel 재배포**
   - Vercel Dashboard → Deployments → 최신 배포 → "Redeploy"
   - 또는 GitHub에 푸시하면 자동 재배포

2. **테스트**
   - 프론트엔드에서 파일 업로드 시도
   - 브라우저 개발자 도구 → Network 탭에서 확인:
     - Status: 200 (성공)
     - Request Headers에 `Content-Type: multipart/form-data; boundary=...` 자동 설정됨

## 추가 확인 사항

### 백엔드 CORS 설정
현재 백엔드는 모든 Origin을 허용하도록 설정되어 있습니다:
```python
allow_origins=["*"]
```

### API 엔드포인트 확인
- 백엔드: `POST /api/analyze`
- 프론트엔드: `${API_BASE_URL}/api/analyze`

### 환경 변수 확인
Vercel에서 `NEXT_PUBLIC_API_URL`이 올바르게 설정되어 있는지 확인:
- 값: `https://checking-ai-production.up.railway.app`
- 재배포 후 적용됨

