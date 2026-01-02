# Railway 백엔드 배포 상세 가이드

## 단계별 설정 방법

### 1단계: 프로젝트 생성

1. [Railway](https://railway.app) 접속 및 로그인
2. 대시보드에서 "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. GitHub 저장소 선택: `seh7un/checkingAI`
5. "Deploy" 또는 "Configure" 클릭

---

### 2단계: Root Directory 설정

**Railway는 자동으로 감지하지만, 수동 설정이 필요할 수 있습니다:**

1. 배포가 시작되면 프로젝트 페이지로 이동
2. **Settings** 탭 클릭 (좌측 메뉴)
3. **Service** 섹션 찾기
4. **Root Directory** 필드 찾기:
   - 기본값: 비어있거나 `/`
   - 변경: `backend` 입력
5. **Save** 클릭

**또는 배포 중 설정:**

1. 배포 로그 화면에서
2. 우측 상단 또는 설정 아이콘 클릭
3. **Root Directory** 설정

---

### 3단계: Start Command 설정

**Railway는 자동으로 감지하지만, 수동 설정:**

1. **Settings** 탭 → **Service** 섹션
2. **Start Command** 필드 찾기:
   - 기본값: 자동 감지된 명령어
   - 변경: `python main.py` 입력
3. **Save** 클릭

**참고:** Railway는 `requirements.txt`를 자동으로 감지하여 의존성을 설치합니다.

---

### 4단계: Environment Variables (환경 변수) 설정

**중요: OpenAI API Key를 여기에 추가해야 합니다!**

1. **Settings** 탭 클릭
2. **Variables** 섹션 찾기 (또는 **Environment** 섹션)
3. **"New Variable"** 또는 **"Add Variable"** 버튼 클릭
4. 다음 변수 추가:

   **변수 1:**
   - **Name**: `OPENAI_API_KEY`
   - **Value**: 실제 OpenAI API Key 입력 (예: `sk-proj-...`)
   - **Add** 또는 **Save** 클릭

   **변수 2 (선택사항):**
   - **Name**: `PORT`
   - **Value**: `8000`
   - Railway가 자동으로 설정하므로 생략 가능

5. 모든 변수 추가 후 **Save** 클릭

---

### 5단계: 도메인 생성

1. **Settings** 탭 → **Networking** 섹션
2. **"Generate Domain"** 버튼 클릭
3. 생성된 URL 확인 (예: `https://your-project.up.railway.app`)
4. 이 URL을 메모해두세요!

---

## Railway UI 화면 설명

### 메인 화면 구성:
```
┌─────────────────────────────────────┐
│  [Project Name]                     │
├─────────────────────────────────────┤
│  [Deployments] [Settings] [Metrics] │  ← 탭 메뉴
├─────────────────────────────────────┤
│                                     │
│  Settings 화면:                     │
│  ┌─────────────────────────────┐   │
│  │ Service                     │   │
│  │  Root Directory: [backend]  │   │
│  │  Start Command: [python...] │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Variables                    │   │
│  │  [New Variable]              │   │
│  │  OPENAI_API_KEY = [값]       │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Networking                  │   │
│  │  [Generate Domain]           │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## 문제 해결

### Root Directory를 찾을 수 없어요
- Settings → Service 섹션 확인
- 또는 배포 로그 화면에서 설정 아이콘 확인
- Railway가 자동으로 감지하는 경우도 있음

### Start Command가 없어요
- Railway는 `requirements.txt`가 있으면 자동으로 Python 앱으로 인식
- `python main.py`가 자동으로 설정될 수 있음
- 수동 설정이 필요하면 Settings → Service에서 확인

### Environment Variables를 어디서 추가하나요?
- Settings 탭 → Variables 섹션
- 또는 Environment Variables 섹션
- "New Variable" 또는 "+" 버튼 클릭

### 배포가 실패해요
- 배포 로그 확인 (Deployments 탭)
- Root Directory가 `backend`로 설정되었는지 확인
- `requirements.txt` 파일이 `backend/` 폴더에 있는지 확인

---

## 빠른 체크리스트

배포 전 확인:
- [ ] GitHub 저장소에 코드가 업로드되어 있음
- [ ] `backend/requirements.txt` 파일 존재
- [ ] `backend/main.py` 파일 존재

Railway 설정:
- [ ] Root Directory: `backend`
- [ ] Start Command: `python main.py` (또는 자동)
- [ ] Environment Variable: `OPENAI_API_KEY` 추가됨
- [ ] 도메인 생성됨

---

## 다음 단계

Railway 배포가 완료되면:
1. 생성된 백엔드 URL 확인
2. `backend/main.py`에서 CORS 설정 업데이트
3. Vercel에서 Frontend 환경 변수 설정

