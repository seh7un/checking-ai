# 커스텀 도메인 설정 가이드

## 개요
현재 도메인:
- **프론트엔드**: `your-project.vercel.app` (Vercel 기본 도메인)
- **백엔드**: `checking-ai-production.up.railway.app` (Railway 기본 도메인)

커스텀 도메인으로 변경하면:
- **프론트엔드**: `yourdomain.com` 또는 `app.yourdomain.com`
- **백엔드**: `api.yourdomain.com` 또는 `backend.yourdomain.com`

---

## 1단계: 도메인 구매 (아직 없다면)

### 추천 도메인 등록소
- **Namecheap**: https://www.namecheap.com
- **Google Domains**: https://domains.google
- **Cloudflare Registrar**: https://www.cloudflare.com/products/registrar

### 도메인 선택 팁
- `.com` 권장 (가장 일반적)
- 짧고 기억하기 쉬운 이름
- 예: `doccheck.com`, `docanalyzer.com`, `safedoc.com`

---

## 2단계: Vercel 커스텀 도메인 설정 (프론트엔드)

### 방법 A: Vercel Dashboard에서 설정

1. **Vercel Dashboard 접속**
   - https://vercel.com/dashboard
   - 프로젝트 선택

2. **Settings → Domains**

3. **도메인 추가**
   - 도메인 입력 (예: `yourdomain.com` 또는 `app.yourdomain.com`)
   - **Add** 클릭

4. **DNS 설정 안내 확인**
   - Vercel이 DNS 레코드를 안내합니다
   - 예:
     ```
     Type: A
     Name: @
     Value: 76.76.21.21
     
     Type: CNAME
     Name: www
     Value: cname.vercel-dns.com
     ```

5. **도메인 등록소에서 DNS 설정**
   - 도메인 등록소 (Namecheap, Google Domains 등) 접속
   - DNS 설정 페이지로 이동
   - Vercel이 안내한 레코드 추가
   - 저장

6. **확인 대기**
   - DNS 전파 시간: 5분 ~ 24시간
   - Vercel Dashboard에서 "Valid Configuration" 확인

### 방법 B: 서브도메인 사용 (권장)

프론트엔드와 백엔드를 분리하려면:

- **프론트엔드**: `app.yourdomain.com` 또는 `www.yourdomain.com`
- **백엔드**: `api.yourdomain.com`

**설정 방법:**
1. Vercel → Settings → Domains
2. `app.yourdomain.com` 추가
3. DNS에 CNAME 레코드 추가:
   ```
   Type: CNAME
   Name: app
   Value: cname.vercel-dns.com
   ```

---

## 3단계: Railway 커스텀 도메인 설정 (백엔드)

### Railway에서 커스텀 도메인 추가

1. **Railway Dashboard 접속**
   - https://railway.app/dashboard
   - 프로젝트 선택

2. **Service 선택** (백엔드 서비스)

3. **Settings → Networking**

4. **Custom Domain 추가**
   - "Add Custom Domain" 클릭
   - 도메인 입력 (예: `api.yourdomain.com`)
   - **Generate** 클릭

5. **DNS 레코드 확인**
   - Railway가 CNAME 레코드를 생성합니다
   - 예:
     ```
     Type: CNAME
     Name: api
     Value: [railway-provided-value].up.railway.app
     ```

6. **도메인 등록소에서 DNS 설정**
   - 도메인 등록소 접속
   - DNS 설정 페이지
   - Railway가 제공한 CNAME 레코드 추가
   - 저장

7. **확인 대기**
   - DNS 전파 시간: 5분 ~ 24시간
   - Railway Dashboard에서 "Active" 상태 확인

---

## 4단계: 환경 변수 업데이트

### Vercel 환경 변수 수정

1. **Vercel Dashboard → Settings → Environment Variables**

2. **`NEXT_PUBLIC_API_URL` 수정**
   - 기존: `https://checking-ai-production.up.railway.app`
   - 새로운: `https://api.yourdomain.com` (또는 설정한 백엔드 도메인)

3. **저장**

4. **재배포**
   - Deployments → 최신 배포 → "..." → "Redeploy"
   - 또는 GitHub 푸시로 자동 재배포

### Railway 환경 변수 (선택사항)

Railway에서도 환경 변수를 설정할 수 있습니다:
- `FRONTEND_URL`: 프론트엔드 도메인 (CORS용)

---

## 5단계: SSL 인증서 (자동)

### Vercel
- ✅ **자동으로 SSL 인증서 발급** (Let's Encrypt)
- 도메인 연결 시 자동 활성화

### Railway
- ✅ **자동으로 SSL 인증서 발급**
- 커스텀 도메인 연결 시 자동 활성화

---

## 예시 설정

### 시나리오: `doccheck.com` 도메인 사용

**DNS 설정 (도메인 등록소):**
```
Type    Name    Value
----    ----    -----
A       @       76.76.21.21          (Vercel)
CNAME   www     cname.vercel-dns.com (Vercel)
CNAME   app     cname.vercel-dns.com (Vercel - 프론트엔드)
CNAME   api     [railway-value].up.railway.app (Railway - 백엔드)
```

**최종 도메인:**
- 프론트엔드: `app.doccheck.com` 또는 `www.doccheck.com`
- 백엔드: `api.doccheck.com`

**환경 변수:**
- Vercel: `NEXT_PUBLIC_API_URL = https://api.doccheck.com`

---

## 비용

### 도메인 구매
- `.com` 도메인: 연간 $10-15 (약 13,000-20,000원)

### Vercel
- ✅ 커스텀 도메인: **무료**
- ✅ SSL 인증서: **무료**

### Railway
- ✅ 커스텀 도메인: **무료**
- ✅ SSL 인증서: **무료**

---

## 문제 해결

### DNS 전파 확인
```bash
# DNS 전파 확인
nslookup app.yourdomain.com
nslookup api.yourdomain.com

# 또는 온라인 도구 사용
# https://dnschecker.org
```

### SSL 인증서 확인
- 브라우저에서 `https://` 접속
- 자물쇠 아이콘 확인
- 인증서 정보 확인

### CORS 오류
- 백엔드 CORS 설정에 새로운 프론트엔드 도메인 추가
- `backend/main.py`의 `FRONTEND_URLS` 업데이트

---

## 빠른 체크리스트

### 도메인 구매
- [ ] 도메인 등록소에서 도메인 구매
- [ ] DNS 설정 권한 확인

### Vercel 설정
- [ ] Vercel → Settings → Domains
- [ ] 도메인 추가
- [ ] DNS 레코드 설정
- [ ] "Valid Configuration" 확인

### Railway 설정
- [ ] Railway → Service → Settings → Networking
- [ ] Custom Domain 추가
- [ ] DNS CNAME 레코드 설정
- [ ] "Active" 상태 확인

### 환경 변수
- [ ] Vercel: `NEXT_PUBLIC_API_URL` 업데이트
- [ ] 재배포 완료

### 테스트
- [ ] 프론트엔드 도메인 접속 확인
- [ ] 백엔드 도메인 접속 확인 (`/` 엔드포인트)
- [ ] 파일 업로드 테스트

---

## 추가 팁

### 서브도메인 vs 루트 도메인

**서브도메인 사용 (권장):**
- `app.yourdomain.com` (프론트엔드)
- `api.yourdomain.com` (백엔드)
- 장점: 명확한 구분, 확장성

**루트 도메인 사용:**
- `yourdomain.com` (프론트엔드)
- `api.yourdomain.com` (백엔드)
- 장점: 더 짧은 URL

### 무료 대안

도메인 구매가 부담스럽다면:
- **Vercel 기본 도메인**: `your-project.vercel.app` (무료, 이미 사용 중)
- **Railway 기본 도메인**: `your-project.up.railway.app` (무료, 이미 사용 중)

현재 설정으로도 충분히 사용 가능합니다!

