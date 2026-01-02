# API URL이 undefined인 경우 해결 방법

## 문제
`window.__API_BASE_URL__`이 `undefined`인 것은 환경 변수가 빌드에 포함되지 않았음을 의미합니다.

## 즉시 확인할 사항

### 1. 파일 업로드 시도
파일을 업로드하면 콘솔에 다음 로그가 나타납니다:

```
🔍 API Request Debug:
  - API Base URL: [이 값이 중요!]
  - Full URL: [전체 URL]
```

**이 로그에서 `API Base URL`이 무엇인지 확인하세요:**
- `https://checking-ai-production.up.railway.app` ✅ (정상)
- `http://localhost:8000` ❌ (환경 변수 미적용)
- `undefined` ❌ (환경 변수 미설정)

### 2. Network 탭 확인
F12 → Network 탭:
1. 파일 업로드 시도
2. `analyze` 요청 찾기
3. **Request URL 확인**:
   - 실제로 어떤 URL로 요청이 가는지 확인
   - `https://checking-ai-production.up.railway.app/api/analyze` ✅
   - `http://localhost:8000/api/analyze` ❌

## 해결 방법

### Vercel 환경 변수 확인 및 설정

1. **Vercel Dashboard 접속**
   - https://vercel.com/dashboard

2. **프로젝트 선택**

3. **Settings → Environment Variables**

4. **환경 변수 확인/추가:**
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://checking-ai-production.up.railway.app`
   - **중요:** Production, Preview, Development **모두**에 체크

5. **저장**

### 재배포 (필수!)

환경 변수를 추가/수정한 후 **반드시 재배포**해야 합니다:

**방법 1: GitHub 푸시 (자동 재배포)**
```bash
git commit --allow-empty -m "Trigger redeploy for env vars"
git push
```

**방법 2: Vercel Dashboard에서 수동 재배포**
- Deployments → 최신 배포 → "..." → "Redeploy"

### 재배포 확인

1. Vercel Dashboard → Deployments
2. 최신 배포 상태 확인:
   - "Building" → 기다림
   - "Ready" → 완료

3. **페이지 새로고침** (Cmd+Shift+R)

4. **다시 확인:**
   ```javascript
   console.log('API URL:', window.__API_BASE_URL__);
   ```
   또는 파일 업로드 시 콘솔 로그 확인

## 빠른 테스트

브라우저 콘솔에서 직접 API 테스트:

```javascript
// 백엔드가 정상 작동하는지 확인
fetch('https://checking-ai-production.up.railway.app')
  .then(r => r.json())
  .then(data => {
    console.log('✅ Backend is working:', data);
  })
  .catch(err => {
    console.error('❌ Backend error:', err);
  });
```

이 테스트가 성공하면 백엔드는 정상입니다.

## 다음 단계

1. **파일 업로드 시도** → 콘솔 로그 확인
2. **Network 탭** → Request URL 확인
3. **결과 공유:**
   - 콘솔의 `API Base URL` 값
   - Network 탭의 Request URL
   - Status Code

이 정보로 정확한 원인을 파악할 수 있습니다!

