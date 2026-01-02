# Vercel 환경 변수 확인 가이드

## 환경 변수가 작동하지 않는 경우

### 1단계: 환경 변수 확인

Vercel Dashboard에서:
1. 프로젝트 선택
2. **Settings** → **Environment Variables**
3. 다음 변수 확인:
   - `NEXT_PUBLIC_API_URL`: `https://checking-ai-production.up.railway.app`
   - 값이 올바른지 확인
   - **중요:** Production, Preview, Development 모두에 설정되어 있는지 확인

### 2단계: 재배포 (필수!)

**환경 변수는 재배포 후에만 적용됩니다!**

1. **Deployments** 탭 클릭
2. 최신 배포 찾기
3. **"Redeploy"** 버튼 클릭
4. 배포 완료까지 대기 (1-2분)

### 3단계: 빌드 로그 확인

1. **Deployments** → 최신 배포 클릭
2. **Build Logs** 확인
3. 환경 변수가 로드되었는지 확인:
   ```
   > Building...
   > NEXT_PUBLIC_API_URL=https://checking-ai-production.up.railway.app
   ```

### 4단계: 브라우저에서 확인

1. 프론트엔드 URL 접속
2. **F12** (개발자 도구) → **Console** 탭
3. 다음 코드 실행:
   ```javascript
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```
   또는
   ```javascript
   console.log(process.env)
   ```

**예상 결과:**
- `https://checking-ai-production.up.railway.app` (정상)
- `undefined` (환경 변수 미적용)

### 5단계: Network 탭 확인

1. 개발자 도구 → **Network** 탭
2. 파일 업로드 시도
3. API 요청 확인:
   - **Request URL**: `https://checking-ai-production.up.railway.app/api/analyze`
   - **Status**: 200 (성공) 또는 에러 코드
   - **Response**: 응답 내용 확인

---

## 문제 해결

### 문제 1: 환경 변수가 undefined

**원인:**
- 재배포하지 않음
- 변수 이름 오타 (`NEXT_PUBLIC_` 접두사 필수)
- Production 환경에 설정하지 않음

**해결:**
1. 변수 이름 확인: `NEXT_PUBLIC_API_URL` (정확히)
2. Production 환경에 설정 확인
3. **재배포 필수**

### 문제 2: CORS 오류

**에러:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**해결:**
- 백엔드 CORS 설정 확인
- 임시로 모든 Origin 허용하도록 수정됨 (개발 단계)

### 문제 3: 404 또는 연결 오류

**해결:**
1. 백엔드 URL이 올바른지 확인
2. 백엔드가 정상 작동하는지 확인:
   ```bash
   curl https://checking-ai-production.up.railway.app
   ```

---

## 빠른 테스트

브라우저 콘솔에서:
```javascript
// 환경 변수 확인
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL)

// API 테스트
fetch('https://checking-ai-production.up.railway.app')
  .then(r => r.json())
  .then(console.log)
```

