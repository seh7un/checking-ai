# 보안 정책 및 가이드라인

## 핵심 보안 원칙

### 1. Zero Storage Policy
- 업로드된 모든 파일은 **절대** 디스크에 저장되지 않습니다
- 모든 처리는 메모리(RAM)에서만 이루어집니다
- 분석 완료 후 즉시 데이터가 휘발됩니다

### 2. 민감 정보 보호

#### 로깅 정책
- 개인정보(전화번호, 주민번호, 이메일 등)는 로그에 기록되지 않습니다
- API Key는 로그에서 자동으로 마스킹됩니다
- 에러 메시지에는 민감 정보가 포함되지 않습니다

#### 로그 마스킹 패턴
- 전화번호: `XXX-XXXX-XXXX`
- 주민등록번호: `XXXXXX-XXXXXXX`
- 이메일: `[EMAIL]`
- 신용카드: `XXXX-XXXX-XXXX-XXXX`
- API Key: `sk-***`

### 3. 입력 검증

#### 파일 검증
- 파일 크기 제한: 최대 10MB
- 허용된 파일 타입만 처리: PDF, TXT, DOCX
- 파일명에 위험한 문자(`..`, `/`, `\`, `\x00`) 차단
- 빈 파일 거부

#### 에러 처리
- 클라이언트에는 일반적인 에러 메시지만 반환
- 상세한 에러 정보는 서버 로그에만 기록
- 스택 트레이스는 클라이언트에 노출되지 않음

### 4. API 보안

#### CORS 설정
- 허용된 Origin만 접근 가능: `http://localhost:3000`
- 프로덕션 환경에서는 실제 도메인으로 변경 필요

#### 타임아웃
- API 요청 타임아웃: 60초
- 타임아웃 초과 시 안전하게 처리

### 5. 환경 변수 보안

#### API Key 관리
- `.env` 파일은 Git에 커밋되지 않음 (`.gitignore`에 포함)
- 환경 변수는 서버 시작 시에만 로드
- API Key는 메모리에만 저장

## 개발 가이드라인

### 로깅 시 주의사항
```python
# ❌ 잘못된 예
logger.info(f"User uploaded file: {file_content}")  # 민감 정보 노출

# ✅ 올바른 예
from utils.logger import safe_log
safe_log(logging.INFO, f"File uploaded: {filename}, size: {size} bytes")
```

### 에러 처리 시 주의사항
```python
# ❌ 잘못된 예
raise HTTPException(status_code=500, detail=str(e))  # 스택 트레이스 노출

# ✅ 올바른 예
from utils.logger import log_error
log_error(e, "Analysis error")
raise HTTPException(status_code=500, detail="An error occurred. Please try again.")
```

## 배포 시 체크리스트

- [ ] `.env` 파일이 Git에 커밋되지 않았는지 확인
- [ ] CORS 설정이 프로덕션 도메인으로 변경되었는지 확인
- [ ] API Key가 안전하게 관리되고 있는지 확인
- [ ] 로그 파일에 민감 정보가 기록되지 않는지 확인
- [ ] 에러 메시지에 민감 정보가 노출되지 않는지 확인

