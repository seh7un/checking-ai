# Railway "Application failed to respond" 해결 가이드

## 문제 원인

Railway에서 애플리케이션이 시작되지 않거나 응답하지 않는 경우:

1. **Root Directory 설정 문제**
2. **Start Command 경로 문제**
3. **PORT 환경 변수 미사용**
4. **의존성 설치 실패**

---

## 해결 방법

### 방법 1: Railway Settings에서 직접 설정 (권장)

1. **Railway Dashboard** → 프로젝트 선택
2. 서비스(Service) 선택
3. **Settings** 탭 클릭

#### Source 섹션:
- **Root Directory**: `backend` 입력
- **Save** 클릭

#### Deploy 섹션:
- **Start Command**: `python main.py` 입력
- **Save** 클릭

#### Variables 섹션:
- `OPENAI_API_KEY` 추가 (이미 있다면 확인)
- **Save** 클릭

4. **Redeploy** 클릭

---

### 방법 2: railway.json 제거 (간단한 방법)

Railway가 자동으로 감지하도록 하려면:

1. `railway.json` 파일 삭제 (또는 무시)
2. Railway Settings에서:
   - Root Directory: `backend`
   - Start Command: `python main.py`
3. 재배포

---

## 확인 사항

### 1. 배포 로그 확인

Railway → Deployments → 최신 배포 → 로그 확인:

**정상적인 로그:**
```
✓ Installing dependencies
✓ Running: python main.py
✓ Application started on port XXXX
```

**문제가 있는 로그:**
```
✗ ModuleNotFoundError: ...
✗ Port already in use
✗ Command not found: python
```

### 2. 서비스 상태 확인

- 서비스가 **Active** 상태인지 확인
- **Stopped** 상태라면 **Restart** 클릭

### 3. Environment Variables 확인

Settings → Variables에서:
- `OPENAI_API_KEY`: 설정되어 있는지 확인
- `PORT`: Railway가 자동 설정 (수동 추가 불필요)

---

## 일반적인 문제

### 문제 1: "python: command not found"

**해결:**
- `runtime.txt` 파일 확인
- 또는 Start Command를 `python3 main.py`로 변경

### 문제 2: "ModuleNotFoundError"

**해결:**
- `requirements.txt`가 `backend/` 폴더에 있는지 확인
- 배포 로그에서 `pip install`이 실행되었는지 확인

### 문제 3: "Port already in use"

**해결:**
- `main.py`에서 PORT 환경 변수를 사용하는지 확인
- 이미 수정됨: `port = int(os.getenv("PORT", 8000))`

---

## 최종 확인

재배포 후 테스트:

```bash
curl https://checking-ai-production.up.railway.app
```

**정상 응답:**
```json
{
    "status": "ok",
    "message": "Stateless Document Analyzer API is running",
    "policy": "Zero Storage - All files processed in memory only"
}
```

---

## Railway Support

문제가 계속되면:
1. 배포 로그 전체 복사
2. Railway Help Station에 문의
3. Request ID 제공: `RUWzM1W9SSKBu9C2V7rehQ`

