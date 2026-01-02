# 배포 문제 해결 가이드

## Vercel 환경 변수 설정 후 작동하지 않는 경우

### 1단계: 환경 변수 확인

**Vercel Dashboard에서:**
1. 프로젝트 선택 → Settings → Environment Variables
2. 다음 변수들이 설정되어 있는지 확인:
   - `NEXT_PUBLIC_API_URL`: `https://checking-ai-production.up.railway.app`
   - `NEXT_PUBLIC_GOOGLE_ADSENSE_ID`: (선택사항)

3. **중요:** 환경 변수는 재배포 후에만 적용됩니다!
   - Deployments 탭 → 최신 배포 → "Redeploy" 클릭

### 2단계: CORS 설정 확인

**백엔드 CORS에 프론트엔드 URL이 포함되어 있어야 합니다:**

`backend/main.py` 파일 확인:
```python
FRONTEND_URLS = [
    "http://localhost:3000",
    "https://your-vercel-url.vercel.app",  # 실제 Vercel URL이 있어야 함
]
```

### 3단계: 브라우저 콘솔 확인

1. 프론트엔드 URL 접속
2. F12 (개발자 도구) → Console 탭
3. 에러 메시지 확인:
   - CORS 오류: 백엔드 CORS 설정 문제
   - Network 오류: 백엔드 URL이 잘못됨
   - 404 오류: API 엔드포인트 경로 문제

### 4단계: Network 탭 확인

1. 개발자 도구 → Network 탭
2. 파일 업로드 시도
3. API 요청 확인:
   - 요청 URL이 올바른지 확인
   - 응답 상태 코드 확인
   - 에러 메시지 확인

---

## 일반적인 문제와 해결책

### 문제 1: CORS 오류

**에러 메시지:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**해결:**
1. `backend/main.py`에서 프론트엔드 URL 추가
2. GitHub에 커밋 및 푸시
3. Railway 자동 재배포 대기

### 문제 2: 404 Not Found

**에러 메시지:**
```
POST https://... 404 (Not Found)
```

**해결:**
1. 백엔드 URL이 올바른지 확인
2. `/api/analyze` 엔드포인트가 존재하는지 확인
3. 백엔드가 정상 작동하는지 확인

### 문제 3: 환경 변수가 적용되지 않음

**증상:**
- 환경 변수를 설정했지만 여전히 `localhost:8000` 사용

**해결:**
1. Vercel에서 환경 변수 저장 확인
2. **재배포 필수**: Deployments → Redeploy
3. 빌드 로그에서 환경 변수 확인

### 문제 4: 백엔드가 응답하지 않음

**해결:**
1. Railway에서 백엔드 상태 확인
2. 배포 로그 확인
3. 백엔드 URL 직접 접속 테스트

---

## 빠른 진단 체크리스트

- [ ] Vercel 환경 변수 `NEXT_PUBLIC_API_URL` 설정됨
- [ ] Vercel 재배포 완료됨
- [ ] 백엔드 CORS에 프론트엔드 URL 추가됨
- [ ] 백엔드가 정상 작동함 (curl 테스트)
- [ ] 브라우저 콘솔에 에러 없음
- [ ] Network 탭에서 API 요청이 전송됨

