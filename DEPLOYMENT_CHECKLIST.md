# 배포 체크리스트

## 사용자가 해야 할 작업들

### ✅ 1단계: GitHub 저장소 생성 및 코드 업로드

**작업:**
1. GitHub 계정 생성/로그인
2. 새 저장소 생성
3. 로컬 코드를 GitHub에 업로드

**명령어:**
```bash
cd "/Users/kimsehyun/Desktop/checking AI"

# Git 초기화 (처음 한 번만)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit"

# GitHub 저장소 연결 (YOUR_USERNAME, YOUR_REPO_NAME 변경)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 업로드
git branch -M main
git push -u origin main
```

---

### ✅ 2단계: Vercel에 Frontend 배포

**작업:**
1. [Vercel](https://vercel.com) 가입/로그인
2. GitHub 저장소 연결
3. 프로젝트 설정:
   - Root Directory: `frontend`
   - Framework: Next.js (자동)
4. 환경 변수 추가 (나중에):
   - `NEXT_PUBLIC_API_URL` (백엔드 URL)
   - `NEXT_PUBLIC_GOOGLE_ADSENSE_ID` (AdSense ID)
5. 배포 완료 후 URL 확인

**결과:**
- 프론트엔드 URL: `https://your-project.vercel.app`
- 이 URL을 메모해두세요!

---

### ✅ 3단계: Railway에 Backend 배포

**작업:**
1. [Railway](https://railway.app) 가입/로그인
2. "New Project" → GitHub 저장소 선택
3. 설정:
   - Root Directory: `backend`
   - Start Command: `python main.py`
4. 환경 변수 추가:
   - `OPENAI_API_KEY`: 기존 API Key
5. 배포 완료 후 도메인 생성
   - Settings → Networking → Generate Domain

**결과:**
- 백엔드 URL: `https://your-project.up.railway.app`
- 이 URL을 메모해두세요!

---

### ✅ 4단계: CORS 설정 업데이트

**작업:**
1. `backend/main.py` 파일 열기
2. 27-33번째 줄의 CORS 설정 수정:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 개발용
        "https://your-frontend-url.vercel.app",  # 실제 프론트엔드 URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

3. GitHub에 커밋 및 푸시:
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push
```

**결과:**
- Railway가 자동으로 재배포합니다

---

### ✅ 5단계: Frontend 환경 변수 설정

**작업:**
1. Vercel Dashboard → 프로젝트 선택
2. Settings → Environment Variables
3. `NEXT_PUBLIC_API_URL` 추가/수정:
   - Value: `https://your-backend-url.railway.app`
4. Save 클릭
5. Deployments → 최신 배포 → Redeploy

**결과:**
- 프론트엔드가 백엔드와 연결됩니다

---

### ✅ 6단계: Google AdSense 설정

**작업:**
1. [Google AdSense](https://www.google.com/adsense/) 가입/로그인
2. "사이트 추가":
   - 실제 프론트엔드 URL 입력 (예: `https://your-project.vercel.app`)
   - 제출
3. 승인 대기 (1-2주)
4. 승인 후:
   - 광고 단위 생성
   - Publisher ID 확인: `ca-pub-XXXXXXXXXX`
   - Slot ID 확인: 숫자
5. Vercel 환경 변수에 추가:
   - `NEXT_PUBLIC_GOOGLE_ADSENSE_ID`: `ca-pub-XXXXXXXXXX`
6. `frontend/app/page.tsx` 64번째 줄 수정:
   ```tsx
   slot="실제SlotID입력"
   ```
7. GitHub에 커밋 및 푸시
8. Vercel 자동 재배포

**결과:**
- 광고가 표시됩니다

---

## 빠른 참조: 필요한 정보들

### 저장해둘 정보
- [ ] GitHub 저장소 URL
- [ ] Vercel 프론트엔드 URL
- [ ] Railway 백엔드 URL
- [ ] Google AdSense Publisher ID
- [ ] Google AdSense Slot ID

---

## 예상 소요 시간

- GitHub 업로드: 10분
- Vercel 배포: 5분
- Railway 배포: 10분
- CORS 설정: 5분
- 환경 변수 설정: 5분
- Google AdSense 승인: 1-2주 (대기)

**총 작업 시간: 약 35분** (AdSense 승인 제외)

---

## 문제 발생 시

### CORS 오류
- 백엔드 CORS에 프론트엔드 URL이 포함되어 있는지 확인
- URL에 `https://` 포함 확인

### API 연결 안됨
- Vercel 환경 변수 `NEXT_PUBLIC_API_URL` 확인
- 백엔드 URL이 올바른지 확인
- Vercel 재배포 필요할 수 있음

### 광고 안나옴
- AdSense 승인 대기 중일 수 있음
- 환경 변수 `NEXT_PUBLIC_GOOGLE_ADSENSE_ID` 확인
- Slot ID가 올바른지 확인

