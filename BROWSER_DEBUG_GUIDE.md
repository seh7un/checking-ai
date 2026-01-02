# 브라우저에서 API URL 확인 가이드

## 문제
브라우저 콘솔에서 `process.env`를 직접 접근할 수 없습니다. Next.js는 빌드 타임에 환경 변수를 정적으로 대체합니다.

## 해결 방법

### 방법 1: 페이지 로드 시 자동 확인 (추가됨)

페이지를 새로고침하면 콘솔에 자동으로 다음 로그가 나타납니다:

```
🌐 Frontend Environment Check:
  - NEXT_PUBLIC_API_URL: [실제 URL]
  - Full API URL: [전체 URL]
  - NODE_ENV: production
```

### 방법 2: 전역 변수로 확인

브라우저 콘솔에서:

```javascript
// API URL 확인
console.log('API URL:', window.__API_BASE_URL__);
```

### 방법 3: 파일 업로드 시 확인

파일을 업로드하면 콘솔에 다음 로그가 나타납니다:

```
🔍 API Request Debug:
  - API Base URL: [URL]
  - Full URL: [전체 URL]
  - File name: [파일명]
📤 Sending request to: [URL]
```

## 다음 단계

1. **페이지 새로고침** (Cmd+Shift+R 또는 Ctrl+Shift+R)
2. **콘솔 확인**: 위의 로그들이 나타나는지 확인
3. **API URL 확인**: 
   - `https://checking-ai-production.up.railway.app`인지 확인
   - `http://localhost:8000`이면 환경 변수 미적용
   - `undefined`이면 환경 변수 미설정

## 환경 변수가 잘못된 경우

### Vercel 환경 변수 확인
1. Vercel Dashboard → 프로젝트 → Settings → Environment Variables
2. `NEXT_PUBLIC_API_URL` 확인
3. 값: `https://checking-ai-production.up.railway.app`
4. **재배포 필수!**

### 재배포 방법
- GitHub에 푸시 (이미 완료)
- 또는 Vercel Dashboard → Deployments → Redeploy

## 확인할 정보

다음 정보를 알려주세요:

1. **페이지 로드 시 콘솔 로그:**
   ```
   🌐 Frontend Environment Check:
     - NEXT_PUBLIC_API_URL: [이 값]
   ```

2. **파일 업로드 시 콘솔 로그:**
   ```
   🔍 API Request Debug:
     - API Base URL: [이 값]
   ```

3. **Network 탭:**
   - Request URL: [실제 요청 URL]
   - Status Code: [에러 코드]

이 정보로 정확한 원인을 파악할 수 있습니다!

