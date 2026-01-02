# 405 에러 심층 해결 가이드

## 문제 상황
프론트엔드에서 파일 업로드 시 계속 405 에러 발생

## 원인 분석

### 1. 백엔드 상태 확인
✅ 백엔드는 정상 작동 중 (curl 테스트 성공)

### 2. 가능한 원인들
1. **환경 변수 미적용**: `NEXT_PUBLIC_API_URL`이 빌드 타임에 제대로 설정되지 않음
2. **Vercel 재배포 미완료**: 변경사항이 아직 배포되지 않음
3. **브라우저 캐시**: 이전 버전의 JavaScript가 캐시됨
4. **Axios 설정 문제**: headers 객체가 문제를 일으킬 수 있음

## 해결 방법

### ✅ 코드 수정 완료
1. **headers 객체 완전 제거**: 빈 headers 객체 대신 아예 제거
2. **디버깅 로그 추가**: 개발 환경에서 API URL 확인 가능
3. **환경 변수 확인 로직 개선**: 클라이언트/서버 사이드 모두 처리

### 다음 단계

#### 1. Vercel 환경 변수 확인 (중요!)
Vercel Dashboard → 프로젝트 → Settings → Environment Variables:
- `NEXT_PUBLIC_API_URL` = `https://checking-ai-production.up.railway.app`
- **Production, Preview, Development 모두에 설정되어 있는지 확인**

#### 2. Vercel 재배포
방법 A: GitHub 푸시 (이미 완료)
- 코드가 GitHub에 푸시되었으므로 자동 재배포 진행 중

방법 B: 수동 재배포
- Vercel Dashboard → Deployments → 최신 배포 → "..." → "Redeploy"

#### 3. 브라우저 캐시 클리어
1. **하드 리프레시**: 
   - Windows/Linux: `Ctrl + Shift + R` 또는 `Ctrl + F5`
   - Mac: `Cmd + Shift + R`
2. **개발자 도구에서 캐시 비활성화**:
   - F12 → Network 탭 → "Disable cache" 체크
   - 페이지 새로고침

#### 4. 브라우저 콘솔 확인
개발자 도구 → Console 탭에서:
```
API Base URL: https://checking-ai-production.up.railway.app
Full URL: https://checking-ai-production.up.railway.app/api/analyze
```
이 로그가 보이면 환경 변수가 제대로 로드된 것입니다.

#### 5. Network 탭에서 실제 요청 확인
개발자 도구 → Network 탭:
1. 파일 업로드 시도
2. `/api/analyze` 요청 찾기
3. 확인 사항:
   - **Request URL**: `https://checking-ai-production.up.railway.app/api/analyze` (올바른지 확인)
   - **Request Method**: `POST` (올바른지 확인)
   - **Status Code**: `200` (성공) 또는 에러 코드
   - **Request Headers**: `Content-Type: multipart/form-data; boundary=...` (자동 설정됨)

## 추가 디버깅

### 환경 변수가 undefined인 경우
브라우저 콘솔에서:
```javascript
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL)
```

**예상 결과:**
- ✅ `https://checking-ai-production.up.railway.app` (정상)
- ❌ `undefined` (환경 변수 미설정 또는 재배포 필요)

### 수동으로 API 테스트
브라우저 콘솔에서:
```javascript
const formData = new FormData();
formData.append('file', new Blob(['test'], { type: 'text/plain' }), 'test.txt');

fetch('https://checking-ai-production.up.railway.app/api/analyze', {
  method: 'POST',
  body: formData
})
.then(r => r.json())
.then(console.log)
.catch(console.error)
```

## 체크리스트

- [ ] Vercel 환경 변수 `NEXT_PUBLIC_API_URL` 설정됨
- [ ] Vercel 재배포 완료됨 (Deployments 탭에서 "Ready" 상태 확인)
- [ ] 브라우저 캐시 클리어됨 (하드 리프레시)
- [ ] 브라우저 콘솔에서 API URL 로그 확인됨
- [ ] Network 탭에서 실제 요청 URL 확인됨
- [ ] 백엔드가 정상 작동함 (curl 테스트 성공)

## 여전히 문제가 있는 경우

1. **Vercel 배포 로그 확인**:
   - Deployments → 최신 배포 → Build Logs
   - 환경 변수가 제대로 로드되었는지 확인

2. **백엔드 로그 확인**:
   - Railway Dashboard → Deployments → Logs
   - 실제 요청이 도착하는지 확인

3. **에러 메시지 공유**:
   - 브라우저 콘솔의 전체 에러 메시지
   - Network 탭의 Response 내용

