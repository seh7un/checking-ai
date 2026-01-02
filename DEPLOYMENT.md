# 배포 가이드

실제 URL로 서비스를 배포하는 방법을 안내합니다.

## 배포 옵션

### 추천 조합
- **Frontend (Next.js)**: Vercel (무료, Next.js 제작사)
- **Backend (FastAPI)**: Railway 또는 Render (무료 플랜 제공)

---

## Part 1: Frontend 배포 (Vercel)

### 1단계: Vercel 계정 생성

1. [Vercel](https://vercel.com) 접속
2. "Sign Up" 클릭
3. GitHub 계정으로 로그인 (권장) 또는 이메일로 가입

### 2단계: 프로젝트 준비

**GitHub에 코드 업로드 (필수)**

1. GitHub에서 새 저장소 생성
   - [GitHub](https://github.com) 접속
   - 우측 상단 "+" → "New repository"
   - Repository name 입력 (예: `document-analyzer`)
   - "Public" 또는 "Private" 선택
   - "Create repository" 클릭

2. 로컬 프로젝트를 GitHub에 업로드

```bash
# 프로젝트 루트에서 실행
cd "/Users/kimsehyun/Desktop/checking AI"

# Git 초기화 (이미 되어있다면 생략)
git init

# .gitignore 확인 (이미 설정됨)
cat .gitignore

# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: Document Analyzer MVP"

# GitHub 저장소 연결 (YOUR_USERNAME과 YOUR_REPO_NAME을 실제 값으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 코드 업로드
git branch -M main
git push -u origin main
```

### 3단계: Vercel에 프로젝트 배포

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. "Add New..." → "Project" 클릭
3. GitHub 저장소 선택
4. 프로젝트 설정:
   - **Framework Preset**: Next.js (자동 감지)
   - **Root Directory**: `frontend` 선택
   - **Build Command**: `npm run build` (자동)
   - **Output Directory**: `.next` (자동)
5. **Environment Variables** 추가:
   - `NEXT_PUBLIC_API_URL`: 백엔드 URL (나중에 설정)
   - `NEXT_PUBLIC_GOOGLE_ADSENSE_ID`: Google AdSense Publisher ID
6. "Deploy" 클릭

### 4단계: 도메인 확인

- 배포 완료 후 `https://your-project.vercel.app` 형식의 URL 제공
- 이 URL을 메모해두세요 (백엔드 CORS 설정에 필요)

---

## Part 2: Backend 배포 (Railway)

### 1단계: Railway 계정 생성

1. [Railway](https://railway.app) 접속
2. "Start a New Project" 클릭
3. GitHub 계정으로 로그인

### 2단계: 프로젝트 배포

1. "New Project" → "Deploy from GitHub repo" 선택
2. GitHub 저장소 선택
3. "Configure" 클릭
4. 설정:
   - **Root Directory**: `backend` 선택
   - **Start Command**: `python main.py`
5. **Environment Variables** 추가:
   - `OPENAI_API_KEY`: OpenAI API Key
   - `PORT`: `8000` (Railway가 자동 설정)

### 3단계: 도메인 확인

1. 배포 완료 후 "Settings" → "Networking"
2. "Generate Domain" 클릭
3. 생성된 URL 확인 (예: `https://your-project.up.railway.app`)
4. 이 URL을 메모해두세요

---

## Part 3: CORS 설정 업데이트

### Backend CORS 설정 변경

`backend/main.py` 파일 수정:

```python
# CORS 설정: 프론트엔드 도메인 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 개발 환경
        "https://your-project.vercel.app",  # 실제 프론트엔드 URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

변경 후 GitHub에 커밋 및 푸시:
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push
```

Railway는 자동으로 재배포합니다.

---

## Part 4: Frontend 환경 변수 업데이트

### Vercel에서 환경 변수 수정

1. Vercel Dashboard → 프로젝트 선택
2. "Settings" → "Environment Variables"
3. `NEXT_PUBLIC_API_URL` 수정:
   - Value: `https://your-backend-url.railway.app`
4. "Save" 클릭
5. "Deployments" → 최신 배포 → "Redeploy" 클릭

---

## Part 5: Google AdSense 설정

### 1단계: AdSense에 실제 URL 등록

1. [Google AdSense](https://www.google.com/adsense/) 접속
2. "사이트" → "사이트 추가"
3. 실제 프론트엔드 URL 입력 (예: `https://your-project.vercel.app`)
4. 제출 후 승인 대기 (1-2주)

### 2단계: 광고 단위 생성

1. AdSense 대시보드 → "광고" → "광고 단위"
2. "새 광고 단위" 생성
3. Publisher ID와 Slot ID 확인

### 3단계: Vercel 환경 변수에 추가

1. Vercel Dashboard → "Settings" → "Environment Variables"
2. `NEXT_PUBLIC_GOOGLE_ADSENSE_ID` 추가:
   - Value: `ca-pub-XXXXXXXXXX` (전체 Publisher ID)
3. `frontend/app/page.tsx`에서 Slot ID 업데이트
4. GitHub에 커밋 및 푸시
5. Vercel 자동 재배포

---

## Part 6: 최종 확인

### 체크리스트

- [ ] Frontend가 Vercel에 배포됨
- [ ] Backend가 Railway에 배포됨
- [ ] CORS 설정이 프론트엔드 URL을 허용함
- [ ] Frontend 환경 변수에 백엔드 URL 설정됨
- [ ] Google AdSense에 실제 URL 등록됨
- [ ] 모든 기능이 정상 작동함

### 테스트

1. 프론트엔드 URL 접속
2. 파일 업로드 테스트
3. 분석 결과 확인
4. 광고 표시 확인

---

## 대안 배포 옵션

### Backend 대안

**Render (무료 플랜)**
1. [Render](https://render.com) 접속
2. "New" → "Web Service"
3. GitHub 저장소 연결
4. 설정:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python main.py`
   - Environment: `Python 3`

**Fly.io (무료 플랜)**
1. [Fly.io](https://fly.io) 접속
2. CLI 설치 및 로그인
3. `fly launch` 실행

### Frontend 대안

**Netlify**
1. [Netlify](https://netlify.com) 접속
2. GitHub 저장소 연결
3. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/.next`

---

## 문제 해결

### CORS 오류
- 백엔드 CORS 설정에 프론트엔드 URL이 포함되어 있는지 확인
- URL 끝에 슬래시(`/`)가 없는지 확인

### 환경 변수 오류
- Vercel/Railway에서 환경 변수가 올바르게 설정되었는지 확인
- 재배포 필요할 수 있음

### API 연결 오류
- 백엔드 URL이 올바른지 확인
- `https://` 프로토콜 사용 확인

---

## 비용

### 무료 플랜
- **Vercel**: 무제한 (개인 프로젝트)
- **Railway**: $5 크레딧/월 (무료 플랜)
- **Render**: 무료 플랜 제공

### 예상 비용
- 개발/테스트: **무료**
- 소규모 프로덕션: **$0-10/월**

