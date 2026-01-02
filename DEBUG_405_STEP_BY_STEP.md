# 405 에러 단계별 디버깅 가이드

## 현재 상황
계속 같은 405 에러가 발생하고 있습니다. 이제 더 상세한 디버깅을 진행합니다.

## 추가된 디버깅 기능

### 1. 백엔드
- ✅ OPTIONS 핸들러 명시적 추가 (CORS preflight 처리)
- ✅ CORS 메서드 명시적 지정

### 2. 프론트엔드
- ✅ 상세한 요청 로그 (항상 출력)
- ✅ 상세한 에러 로그
- ✅ 실제 요청 URL 확인

## 즉시 확인할 사항

### 1단계: 브라우저 콘솔 확인

**F12 → Console 탭**에서 다음 로그들을 확인하세요:

```
🔍 API Request Debug:
  - API Base URL: https://checking-ai-production.up.railway.app
  - Full URL: https://checking-ai-production.up.railway.app/api/analyze
  - File name: test.txt
  - File size: 1234
  - File type: text/plain
📤 Sending request to: https://checking-ai-production.up.railway.app/api/analyze
```

**이 로그가 보이지 않으면:**
- Vercel 재배포가 완료되지 않았을 수 있습니다
- 브라우저 캐시를 클리어하세요 (Cmd+Shift+R)

**이 로그에서 URL이 잘못되었으면:**
- `API Base URL`이 `undefined` 또는 `http://localhost:8000`인 경우
- → Vercel 환경 변수 `NEXT_PUBLIC_API_URL`이 설정되지 않았거나 재배포가 필요합니다

### 2단계: Network 탭 확인

**F12 → Network 탭**에서:

1. **파일 업로드 시도**
2. **`analyze` 요청 찾기** (필터에 `analyze` 입력)
3. **요청 클릭하여 상세 정보 확인:**

   **Headers 탭:**
   - Request URL: `https://checking-ai-production.up.railway.app/api/analyze` ✅
   - Request Method: `POST` ✅
   - Content-Type: `multipart/form-data; boundary=...` ✅

   **Response 탭:**
   - Status Code: `405 Method Not Allowed` ❌
   - Response 내용 확인

   **Preview 탭:**
   - 에러 메시지 확인

### 3단계: 에러 로그 확인

콘솔에서 다음 로그를 확인하세요:

```
❌ API Error Details:
  - Error: [에러 객체]
  - Response: [응답 객체]
  - Status: 405
  - Status Text: Method Not Allowed
  - Data: [응답 데이터]
  - Request URL: [실제 요청 URL]
  - Request Method: POST
```

**이 정보를 복사해서 알려주세요!**

## 가능한 원인과 해결책

### 원인 1: 환경 변수 미적용
**증상:** 콘솔에서 `API Base URL: undefined` 또는 `http://localhost:8000`

**해결:**
1. Vercel Dashboard → Settings → Environment Variables
2. `NEXT_PUBLIC_API_URL` 확인
3. 값: `https://checking-ai-production.up.railway.app`
4. **재배포 필수!**

### 원인 2: Vercel 재배포 미완료
**증상:** 최신 코드가 반영되지 않음

**해결:**
1. Vercel Dashboard → Deployments
2. 최신 배포 상태 확인
3. "Building" → 기다림
4. "Ready" → 테스트

### 원인 3: 백엔드 라우팅 문제
**증상:** 요청 URL은 올바른데 405 에러

**해결:**
- 백엔드에 OPTIONS 핸들러 추가 완료
- Railway 재배포 확인 필요

### 원인 4: CORS preflight 실패
**증상:** OPTIONS 요청이 실패

**해결:**
- 백엔드에 OPTIONS 핸들러 추가 완료
- Railway 재배포 확인 필요

## 다음 단계

1. **브라우저 콘솔 로그 확인**
   - 위의 로그들이 보이는지 확인
   - URL이 올바른지 확인

2. **Network 탭 확인**
   - 실제 요청 URL 확인
   - Status Code 확인
   - Response 내용 확인

3. **결과 공유**
   - 콘솔 로그 복사
   - Network 탭의 Request/Response 정보
   - 스크린샷 (가능하면)

## 빠른 테스트

브라우저 콘솔에서 직접 테스트:

```javascript
// 1. 환경 변수 확인
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

// 2. 직접 API 테스트
fetch('https://checking-ai-production.up.railway.app')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// 3. FormData 테스트
const formData = new FormData();
formData.append('file', new Blob(['test'], { type: 'text/plain' }), 'test.txt');

fetch('https://checking-ai-production.up.railway.app/api/analyze', {
  method: 'POST',
  body: formData
})
.then(r => {
  console.log('Status:', r.status);
  console.log('Status Text:', r.statusText);
  return r.text();
})
.then(text => {
  console.log('Response:', text);
})
.catch(console.error);
```

이 테스트 결과도 알려주세요!

