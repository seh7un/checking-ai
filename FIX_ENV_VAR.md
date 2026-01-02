# 환경 변수 수정 가이드 (프로토콜 추가)

## 문제 발견!
환경 변수에 `https://` 프로토콜이 빠져있습니다!

**현재 (잘못됨):**
```
NEXT_PUBLIC_API_URL = checking-ai-production.up.railway.app
```

**올바른 값:**
```
NEXT_PUBLIC_API_URL = https://checking-ai-production.up.railway.app
```

## 수정 방법

### 1. Vercel Dashboard 접속
1. https://vercel.com/dashboard
2. 프로젝트 선택

### 2. 환경 변수 수정
1. **Settings** → **Environment Variables**
2. `NEXT_PUBLIC_API_URL` 찾기
3. **Edit** 클릭 (또는 삭제 후 재생성)
4. **Value** 수정:
   ```
   https://checking-ai-production.up.railway.app
   ```
   ⚠️ **반드시 `https://` 포함!**
5. **Production, Preview, Development 모두 체크**
6. **Save** 클릭

### 3. 재배포 (필수!)
환경 변수를 수정한 후 **반드시 재배포**해야 합니다:

**방법 A: 자동 재배포 (GitHub 푸시)**
- 빈 커밋 푸시하면 자동 재배포됩니다

**방법 B: 수동 재배포**
- Vercel Dashboard → Deployments → 최신 배포 → "..." → "Redeploy"

### 4. 확인
재배포 완료 후:
1. 페이지 새로고침 (Cmd+Shift+R)
2. 콘솔 확인:
   ```
   🔧 API Base URL (from build): https://checking-ai-production.up.railway.app
   ```
   ✅ `https://`가 포함되어 있어야 함!

3. 파일 업로드 테스트
   - 이제 정상 작동해야 합니다!

## 빠른 확인 체크리스트

- [ ] Vercel 환경 변수에 `https://` 포함됨
- [ ] Production, Preview, Development 모두 설정됨
- [ ] 재배포 완료됨
- [ ] 콘솔에서 `https://` 확인됨
- [ ] 파일 업로드 테스트 성공

