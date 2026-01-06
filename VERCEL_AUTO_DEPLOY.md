# Vercel 자동 배포 가이드

## 자동 배포 (일반적인 경우)

### ✅ GitHub 푸시 시 자동 재배포

**대부분의 경우 수동 redeploy가 필요 없습니다!**

Vercel은 GitHub 저장소와 연결되어 있으면 **자동으로 재배포**합니다:

```bash
# 코드 수정 후
git add .
git commit -m "변경사항 설명"
git push  # ← 이것만 하면 자동 재배포!
```

**자동 재배포가 트리거되는 경우:**
- ✅ 코드 변경 후 GitHub에 푸시
- ✅ 새로운 커밋이 main/master 브랜치에 푸시
- ✅ Pull Request 머지

**재배포 확인:**
1. Vercel Dashboard → Deployments
2. 새로운 배포가 자동으로 시작됨
3. 상태: "Building" → "Ready"

---

## 수동 Redeploy가 필요한 경우

다음 경우에만 수동으로 redeploy가 필요합니다:

### 1. 환경 변수 변경 후

**환경 변수는 빌드 타임에 적용되므로 재배포가 필요합니다.**

**방법 A: GitHub 푸시 (권장)**
```bash
git commit --allow-empty -m "Trigger redeploy for env vars"
git push
```

**방법 B: Vercel Dashboard에서 수동 재배포**
- Deployments → 최신 배포 → "..." → "Redeploy"

### 2. 자동 배포가 실패한 경우

- 빌드 오류가 발생했을 때
- 수정 후 수동으로 재배포 시도

### 3. 특정 커밋으로 재배포하고 싶을 때

- 이전 버전으로 롤백하고 싶을 때
- 특정 커밋으로 재배포하고 싶을 때

---

## 일반적인 워크플로우

### 코드 수정 시

```bash
# 1. 코드 수정
# (파일 편집)

# 2. 변경사항 커밋
git add .
git commit -m "기능 추가: 계약서 분석 개선"

# 3. GitHub에 푸시
git push

# 4. 끝! Vercel이 자동으로 재배포합니다
# (Vercel Dashboard에서 진행 상황 확인)
```

### 환경 변수 변경 시

```bash
# 1. Vercel Dashboard에서 환경 변수 수정
# Settings → Environment Variables

# 2. 재배포 트리거
git commit --allow-empty -m "Trigger redeploy for env vars"
git push

# 또는 Vercel Dashboard에서 수동 Redeploy
```

---

## 배포 상태 확인

### Vercel Dashboard에서 확인

1. **Deployments 탭**
   - 최신 배포 상태 확인
   - "Building" = 배포 진행 중
   - "Ready" = 배포 완료
   - "Error" = 배포 실패 (로그 확인)

2. **배포 로그 확인**
   - 배포 항목 클릭
   - Build Logs 확인
   - 에러 발생 시 로그 확인

### 이메일 알림 (선택사항)

- Vercel Settings → Notifications
- 배포 완료/실패 시 이메일 알림 설정 가능

---

## 자동 배포 설정 확인

### Vercel과 GitHub 연결 확인

1. Vercel Dashboard → 프로젝트 → Settings
2. **Git** 섹션 확인
3. 연결된 저장소 확인
4. **Auto-deploy** 설정 확인 (기본적으로 활성화됨)

### 자동 배포 비활성화 (필요한 경우)

- Settings → Git → "Auto-deploy" 체크 해제
- 수동 배포만 원할 때 사용

---

## 빠른 참조

### ✅ 자동 재배포 (일반적인 경우)
```bash
git push  # 이것만 하면 됨!
```

### ⚠️ 수동 재배포가 필요한 경우
1. 환경 변수 변경 후
2. 자동 배포 실패 시
3. 특정 커밋으로 재배포하고 싶을 때

### 🔍 배포 확인
- Vercel Dashboard → Deployments
- 상태: "Building" → "Ready"

---

## 팁

### 배포 속도 향상

- **Incremental Static Regeneration (ISR)** 사용
- **Edge Functions** 활용
- 불필요한 파일 제외 (`.vercelignore`)

### 배포 전 테스트

- 로컬에서 `npm run build` 실행
- 빌드 오류 사전 확인

### 롤백

- Deployments → 이전 배포 → "..." → "Promote to Production"

---

## 요약

**대부분의 경우:**
- ✅ GitHub 푸시만 하면 자동 재배포
- ❌ 수동 redeploy 불필요

**수동 redeploy가 필요한 경우:**
- 환경 변수 변경 후
- 자동 배포 실패 시
- 특정 커밋으로 재배포하고 싶을 때

**결론:** 코드 수정 후 `git push`만 하면 됩니다! 🚀

