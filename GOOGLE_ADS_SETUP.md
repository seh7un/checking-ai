# Google AdSense 설정 가이드

## 1. Google AdSense 계정 생성 및 승인

### 단계별 가이드

1. **Google AdSense 계정 생성**
   - [Google AdSense](https://www.google.com/adsense/) 방문
   - Google 계정으로 로그인
   - "시작하기" 클릭
   - 웹사이트 URL 입력 (예: `http://localhost:3000` 또는 실제 도메인)
   - 계정 정보 입력

2. **사이트 승인 대기**
   - Google이 사이트를 검토합니다 (보통 1-2주 소요)
   - 승인되면 이메일로 알림을 받습니다
   - 승인 전까지는 테스트 광고만 표시됩니다

## 2. 광고 단위 생성

1. **AdSense 대시보드 접속**
   - [AdSense 대시보드](https://www.google.com/adsense/) 로그인

2. **광고 단위 생성**
   - 좌측 메뉴에서 "광고" 클릭
   - "광고 단위" 클릭
   - "새 광고 단위" 클릭
   - 광고 단위 이름 입력 (예: "메인 페이지 배너")
   - 광고 형식 선택:
     - **반응형 광고**: 자동으로 크기 조절 (권장)
     - **표시 광고**: 고정 크기
   - "광고 단위 만들기" 클릭

3. **광고 코드 확인**
   - 생성된 광고 단위에서 다음 정보 확인:
     - **Publisher ID**: `ca-pub-XXXXXXXXXX` 형식
     - **Slot ID**: 숫자로 된 광고 슬롯 ID

## 3. 환경 변수 설정

### 프론트엔드 `.env.local` 파일 생성

프로젝트 루트에 `.env.local` 파일을 생성하고 다음 내용을 추가:

```bash
# Google AdSense Publisher ID
NEXT_PUBLIC_GOOGLE_ADSENSE_ID=ca-pub-XXXXXXXXXX
```

**중요:**
- `ca-pub-` 접두사 포함하여 전체 Publisher ID 입력
- 파일은 Git에 커밋하지 마세요 (`.gitignore`에 포함됨)

### 예시

```bash
NEXT_PUBLIC_GOOGLE_ADSENSE_ID=ca-pub-1234567890123456
```

## 4. 광고 슬롯 ID 설정

`frontend/app/page.tsx` 파일에서 광고 슬롯 ID를 업데이트:

```tsx
<GoogleAds 
  slot="1234567890" // 여기에 실제 Slot ID 입력
  format="auto"
  className="min-h-[100px]"
/>
```

## 5. 서버 재시작

환경 변수를 변경한 후 개발 서버를 재시작:

```bash
cd frontend
npm run dev
```

## 6. 광고 표시 확인

1. 브라우저에서 `http://localhost:3000` 접속
2. 광고가 표시되는지 확인
3. 개발자 도구(F12)에서 콘솔 에러 확인

## 문제 해결

### 광고가 표시되지 않는 경우

1. **Publisher ID 확인**
   - `.env.local` 파일에 올바른 Publisher ID가 있는지 확인
   - `ca-pub-` 접두사 포함 확인

2. **Slot ID 확인**
   - `page.tsx`에서 올바른 Slot ID 사용 확인

3. **AdSense 승인 상태 확인**
   - AdSense 대시보드에서 계정 상태 확인
   - 승인 대기 중이면 테스트 광고만 표시됨

4. **콘솔 에러 확인**
   - 브라우저 개발자 도구에서 에러 메시지 확인
   - CORS 또는 스크립트 로드 에러 확인

5. **광고 차단기 확인**
   - 브라우저 광고 차단 확장 프로그램 비활성화

### 개발 환경에서 광고가 보이지 않는 경우

- Google AdSense는 실제 도메인에서만 정상 작동합니다
- `localhost`에서는 제한적으로 작동할 수 있습니다
- 프로덕션 환경에 배포 후 테스트하는 것을 권장합니다

## 광고 배치 위치

현재 광고는 다음 위치에 배치되어 있습니다:

1. **메인 페이지 상단**: 파일 업로드 섹션 위
2. 추가 위치가 필요하면 `GoogleAds` 컴포넌트를 다른 위치에 추가

## 광고 형식 옵션

`format` prop으로 광고 형식을 지정할 수 있습니다:

- `auto`: 반응형 (권장)
- `rectangle`: 직사각형
- `vertical`: 세로형
- `horizontal`: 가로형

## 참고 자료

- [Google AdSense 도움말](https://support.google.com/adsense)
- [AdSense 정책](https://support.google.com/adsense/answer/48182)
- [Next.js 환경 변수 가이드](https://nextjs.org/docs/basic-features/environment-variables)

