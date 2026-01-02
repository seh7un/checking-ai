# Railway 배포 문제 해결 가이드

## 현재 상황: "Application not found" (404 오류)

### 가능한 원인들

1. **배포가 아직 완료되지 않음**
2. **서비스가 실행되지 않음**
3. **Root Directory 설정 문제**
4. **도메인 설정 문제**

---

## 해결 방법

### 1단계: Railway에서 배포 상태 확인

1. Railway Dashboard 접속
2. 프로젝트 선택
3. **Deployments** 탭 확인
4. 최신 배포 상태 확인:
   - ✅ **Success**: 배포 성공
   - ⏳ **Building/Deploying**: 배포 진행 중 (대기)
   - ❌ **Failed**: 배포 실패 (로그 확인 필요)

### 2단계: 서비스 상태 확인

1. 프로젝트 메인 페이지에서
2. 서비스(Service) 카드 확인
3. 상태 확인:
   - 🟢 **Active**: 정상 실행 중
   - 🔴 **Stopped**: 중지됨 (재시작 필요)
   - 🟡 **Building**: 빌드 중

### 3단계: Root Directory 확인

1. 서비스 선택 → **Settings** 탭
2. **Source** 섹션 확인
3. **Root Directory**가 `backend`로 설정되어 있는지 확인
4. 설정되어 있지 않으면 `backend` 입력 후 **Save**

### 4단계: 배포 로그 확인

1. **Deployments** 탭
2. 최신 배포 클릭
3. 로그 확인:
   - `cd backend` 명령어가 실행되는지 확인
   - `pip install -r requirements.txt` 실행되는지 확인
   - `python main.py` 실행되는지 확인
   - 에러 메시지 확인

### 5단계: 도메인 재생성

1. **Settings** → **Networking** 섹션
2. 기존 도메인 삭제 (있다면)
3. **"Generate Domain"** 클릭
4. 새 도메인 확인

---

## 일반적인 문제와 해결책

### 문제 1: 배포가 계속 실패함

**해결:**
- 배포 로그에서 에러 메시지 확인
- `requirements.txt` 파일이 `backend/` 폴더에 있는지 확인
- `main.py` 파일이 `backend/` 폴더에 있는지 확인

### 문제 2: 서비스가 시작되지 않음

**해결:**
- **Settings** → **Deploy** 섹션
- **Start Command** 확인: `python main.py`
- **Restart** 버튼 클릭

### 문제 3: 도메인이 작동하지 않음

**해결:**
- **Settings** → **Networking**
- 도메인 삭제 후 재생성
- 몇 분 대기 후 다시 시도

---

## 빠른 체크리스트

- [ ] 배포가 성공적으로 완료되었는가?
- [ ] 서비스가 Active 상태인가?
- [ ] Root Directory가 `backend`로 설정되어 있는가?
- [ ] Start Command가 `python main.py`인가?
- [ ] Environment Variables에 `OPENAI_API_KEY`가 설정되어 있는가?
- [ ] 도메인이 생성되어 있는가?

---

## 정상 작동 시 표시되는 내용

백엔드가 정상 작동하면 다음 JSON이 표시됩니다:

```json
{
    "status": "ok",
    "message": "Stateless Document Analyzer API is running",
    "policy": "Zero Storage - All files processed in memory only"
}
```

