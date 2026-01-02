# Vercel 재배포 가이드 (Redeploy 버튼 찾기)

## 방법 1: Deployments 탭에서 재배포 (권장)

### 단계별 설명

1. **Vercel Dashboard 접속**
   - https://vercel.com/dashboard 접속
   - 로그인 (GitHub 계정으로 로그인)

2. **프로젝트 선택**
   - 대시보드에서 배포한 프로젝트 클릭
   - 프로젝트 이름을 클릭하면 프로젝트 상세 페이지로 이동

3. **Deployments 탭 찾기**
   - 프로젝트 상세 페이지 상단에 여러 탭이 있습니다:
     - **Overview** (개요)
     - **Deployments** (배포) ← **여기 클릭!**
     - **Analytics** (분석)
     - **Settings** (설정)
     - **Insights** (인사이트)
   
   - **"Deployments"** 탭을 클릭합니다

4. **배포 목록 확인**
   - Deployments 탭에서 최근 배포 목록이 보입니다
   - 각 배포 항목에는 다음 정보가 표시됩니다:
     - 배포 상태 (Ready, Building, Error 등)
     - 배포 시간
     - Git 커밋 메시지
     - 브랜치 이름

5. **최신 배포 찾기**
   - 목록 맨 위에 있는 가장 최근 배포를 찾습니다
   - 상태가 "Ready" 또는 "Error"인 배포를 선택합니다

6. **Redeploy 버튼 찾기**
   - 배포 항목을 클릭하면 배포 상세 페이지로 이동합니다
   - 또는 배포 항목 오른쪽에 **"..." (점 3개)** 메뉴가 있을 수 있습니다
   - **"..." 메뉴를 클릭**하면 다음 옵션들이 나타납니다:
     - **Redeploy** ← **이것을 클릭!**
     - Cancel Deployment
     - Download Logs
     - 등등

7. **Redeploy 확인**
   - "Redeploy"를 클릭하면 확인 메시지가 나타날 수 있습니다
   - 확인하면 재배포가 시작됩니다

---

## 방법 2: GitHub에서 푸시로 자동 재배포

Vercel은 GitHub와 연결되어 있으므로, 코드를 푸시하면 자동으로 재배포됩니다.

### 단계

1. **코드 변경 확인**
   - 이미 `frontend/lib/api.ts`를 수정하고 GitHub에 푸시했습니다
   - 따라서 자동 재배포가 진행 중일 수 있습니다

2. **자동 재배포 확인**
   - Vercel Dashboard → 프로젝트 → Deployments 탭
   - 최신 배포 항목을 확인합니다
   - 상태가 "Building" 또는 "Ready"로 변경되는지 확인합니다

---

## 방법 3: Settings에서 재배포 트리거

1. **Settings 탭 클릭**
   - 프로젝트 상세 페이지 → **Settings** 탭

2. **Git 설정 확인**
   - Settings → **Git** 섹션
   - 연결된 저장소 확인

3. **수동 재배포**
   - Settings → **Deployments** 섹션
   - "Redeploy" 버튼이 있을 수 있습니다

---

## 시각적 가이드 (텍스트 설명)

```
Vercel Dashboard
├── 프로젝트 목록
│   └── [프로젝트 이름] 클릭
│       │
│       ├── Overview 탭
│       ├── Deployments 탭 ← 여기 클릭!
│       │   │
│       │   └── 배포 목록
│       │       └── [최신 배포 항목]
│       │           │
│       │           └── "..." (점 3개) 메뉴 클릭
│       │               │
│       │               └── "Redeploy" 클릭 ← 여기!
│       │
│       ├── Analytics 탭
│       ├── Settings 탭
│       └── Insights 탭
```

---

## 재배포 확인 방법

재배포가 시작되면:

1. **Deployments 탭에서 확인**
   - 새로운 배포 항목이 생성됩니다
   - 상태가 "Building" → "Ready"로 변경됩니다

2. **배포 로그 확인**
   - 배포 항목을 클릭하면 상세 로그를 볼 수 있습니다
   - 빌드 과정과 환경 변수 로드 여부를 확인할 수 있습니다

3. **완료 확인**
   - 상태가 "Ready"가 되면 재배포 완료
   - 프론트엔드 URL에서 테스트 가능

---

## 문제 해결

### "Redeploy" 버튼이 보이지 않는 경우

1. **권한 확인**
   - 프로젝트 소유자 또는 관리자 권한이 필요합니다
   - 팀 프로젝트인 경우 권한을 확인하세요

2. **배포 상태 확인**
   - 배포가 이미 진행 중이면 "Redeploy" 버튼이 비활성화될 수 있습니다
   - 기다렸다가 다시 시도하세요

3. **GitHub 푸시 사용**
   - 버튼을 찾기 어려우면 GitHub에 빈 커밋을 푸시하면 자동 재배포됩니다:
   ```bash
   git commit --allow-empty -m "Trigger redeploy"
   git push
   ```

---

## 빠른 확인 체크리스트

- [ ] Vercel Dashboard에 로그인됨
- [ ] 프로젝트 선택됨
- [ ] Deployments 탭 클릭됨
- [ ] 최신 배포 항목 확인됨
- [ ] "..." 메뉴 또는 Redeploy 버튼 찾음
- [ ] 재배포 시작됨
- [ ] 배포 상태 확인 중

---

## 추가 팁

### 자동 재배포 확인
이미 GitHub에 푸시했으므로, Vercel Dashboard → Deployments 탭에서 새로운 배포가 자동으로 시작되었는지 확인하세요.

### 배포 상태 확인
- **Building**: 배포 진행 중
- **Ready**: 배포 완료 (사용 가능)
- **Error**: 배포 실패 (로그 확인 필요)
- **Canceled**: 배포 취소됨

