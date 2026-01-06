# Instagram 크롤러 Selenium 설정 가이드

## 개선 사항

[참고 블로그 포스트](https://hamhands.tistory.com/entry/챗gpt로-인스타그램-크롤링-하기인스타-api-없이-크롤링-성공)를 참고하여 Selenium을 추가했습니다.

## Selenium이 필요한 이유

Instagram은 JavaScript로 동적 렌더링을 하기 때문에:
- 단순 HTTP 요청만으로는 데이터를 가져오기 어려움
- 페이지가 완전히 로드된 후에야 데이터가 표시됨
- Selenium은 실제 브라우저를 제어하여 JavaScript 실행 후 데이터 추출 가능

## 설치된 라이브러리

- `selenium==4.15.2`: 웹 브라우저 자동화
- `webdriver-manager==4.0.1`: ChromeDriver 자동 관리

## 작동 방식

1. **Selenium 우선 사용** (기본값)
   - Chrome 브라우저를 헤드리스 모드로 실행
   - 페이지 로드 후 JavaScript 실행 대기
   - XPath를 사용하여 좋아요, 댓글 수 추출

2. **폴백: requests + HTML 파싱**
   - Selenium 실패 시 자동으로 폴백
   - oEmbed API + HTML 파싱 사용

## 서버 환경 설정

### Railway/Render 등 클라우드 환경

Selenium을 사용하려면 Chrome 브라우저가 필요합니다:

```bash
# Dockerfile 또는 빌드 스크립트에 추가
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*
```

또는 Railway/Render의 경우:
- Buildpack에 Chrome 추가 필요
- 또는 Selenium 없이 requests 방식 사용

### 로컬 환경

자동으로 ChromeDriver가 설치됩니다 (webdriver-manager).

## 환경 변수

선택사항:
- `INSTAGRAM_ACCESS_TOKEN`: Instagram Graph API 토큰 (향후 지원)

## 사용 방법

```python
from utils.instagram_crawler import crawl_instagram_post

# Selenium 사용 (기본값)
data = crawl_instagram_post("https://www.instagram.com/p/ABC123/")

# Selenium 없이 사용
data = crawl_instagram_post("https://www.instagram.com/p/ABC123/", use_selenium=False)
```

## 문제 해결

### ChromeDriver 오류

```bash
# webdriver-manager가 자동으로 설치하지만, 수동 설치도 가능
pip install webdriver-manager
```

### 헤드리스 모드 오류

서버 환경에서 Chrome이 없으면:
- Selenium 비활성화: `use_selenium=False`
- 또는 Chrome 설치 (위의 Dockerfile 참고)

## 성능

- **Selenium**: 느리지만 정확 (5-10초)
- **requests**: 빠르지만 제한적 (1-2초)

## 참고

- Instagram의 HTML 구조가 변경되면 선택자 업데이트 필요
- 비공개 계정은 크롤링 불가
- Instagram 이용약관 준수 필요

