# Vercel 빌드 오류 해결 가이드

## 문제
```
Command "cd frontend && npm install" exited with 1
```

## 원인
Vercel Dashboard에서 **Root Directory**를 `frontend`로 설정한 경우, `vercel.json`의 명령어에서 `cd frontend`가 불필요하거나 오류를 일으킬 수 있습니다.

## 해결 방법

### 방법 1: vercel.json 수정 (권장)

`vercel.json` 파일을 수정했습니다:
- `installCommand`: `npm install` (cd frontend 제거)
- `buildCommand`: `npm run build` (cd frontend 제거)
- `outputDirectory`: `.next` (frontend/.next에서 frontend 제거)

**이유:** Vercel Dashboard에서 Root Directory를 `frontend`로 설정하면, 모든 명령어는 이미 `frontend` 디렉토리에서 실행됩니다.

### 방법 2: Vercel Dashboard에서 Root Directory 확인

1. Vercel Dashboard → 프로젝트 → Settings
2. **General** → **Root Directory** 확인
3. `frontend`로 설정되어 있는지 확인

**Root Directory가 `frontend`인 경우:**
- `vercel.json`의 명령어에서 `cd frontend` 제거 필요 ✅ (이미 수정됨)

**Root Directory가 빈 값(루트)인 경우:**
- `vercel.json`의 명령어에 `cd frontend` 필요
- 또는 Root Directory를 `frontend`로 변경

## 확인 사항

### 1. package.json 위치
- `frontend/package.json`이 존재하는지 확인 ✅

### 2. Node.js 버전
- Vercel은 자동으로 Node.js 버전을 감지합니다
- 필요시 `.nvmrc` 파일 추가 가능

### 3. 빌드 로그 확인
- Vercel Dashboard → Deployments → 최신 배포 → Build Logs
- 정확한 오류 메시지 확인

## 추가 문제 해결

### npm install 실패 시

**가능한 원인:**
1. `package-lock.json` 손상
2. Node.js 버전 불일치
3. 의존성 충돌

**해결:**
```bash
# 로컬에서 테스트
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 빌드 명령어 오류 시

**확인:**
- `frontend/package.json`의 `build` 스크립트 확인
- `next build` 명령어가 정상 작동하는지 확인

## 최종 확인

1. **GitHub에 푸시**
   ```bash
   git add vercel.json
   git commit -m "Fix Vercel build command"
   git push
   ```

2. **Vercel 자동 재배포 확인**
   - Vercel Dashboard → Deployments
   - 새로운 배포 시작 확인
   - 빌드 성공 여부 확인

3. **빌드 로그 확인**
   - 배포 클릭 → Build Logs
   - `npm install` 성공 확인
   - `npm run build` 성공 확인

## 참고

### Vercel 설정 우선순위
1. `vercel.json` 파일
2. Vercel Dashboard 설정
3. 자동 감지

**Root Directory 설정:**
- Dashboard에서 설정한 Root Directory가 우선
- `vercel.json`의 명령어는 Root Directory 기준으로 실행됨

