# Railway 백엔드 URL 테스트 가이드

## 백엔드 URL 접속 시 표시되는 내용

### 정상 작동 시

Railway 백엔드 URL (예: `https://your-project.up.railway.app`)에 브라우저로 접속하면:

```json
{
    "status": "ok",
    "message": "Stateless Document Analyzer API is running",
    "policy": "Zero Storage - All files processed in memory only"
}
```

이 JSON 응답이 표시되면 **정상 작동** 중입니다! ✅

---

## 확인 방법

### 1. 브라우저에서 접속
- URL을 브라우저 주소창에 입력
- JSON 형식의 응답이 보이면 정상

### 2. curl 명령어로 테스트
```bash
curl https://your-project.up.railway.app
```

예상 출력:
```json
{"status":"ok","message":"Stateless Document Analyzer API is running","policy":"Zero Storage - All files processed in memory only"}
```

### 3. Health Check 엔드포인트
```bash
curl https://your-project.up.railway.app/
```

---

## 문제 해결

### ❌ "This site can't be reached" 또는 연결 오류
- Railway 배포가 완료되지 않았을 수 있음
- Deployments 탭에서 배포 상태 확인
- 배포가 진행 중이면 완료까지 대기

### ❌ "404 Not Found"
- Root Directory가 올바르게 설정되지 않았을 수 있음
- Settings → Source → Root Directory가 `backend`인지 확인

### ❌ "500 Internal Server Error"
- 배포 로그 확인 (Deployments 탭)
- Environment Variables 확인 (OPENAI_API_KEY 등)
- `requirements.txt` 파일이 올바른지 확인

### ❌ 빈 화면 또는 다른 내용
- 배포가 아직 진행 중일 수 있음
- 몇 분 후 다시 시도

---

## 다음 단계

백엔드 URL이 정상 작동하면:
1. ✅ 백엔드 URL 메모
2. ✅ `backend/main.py`에서 CORS 설정 업데이트
3. ✅ Vercel에서 Frontend 환경 변수 설정

