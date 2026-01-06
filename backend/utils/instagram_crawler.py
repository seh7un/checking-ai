"""
인스타그램 크롤링 모듈
Instagram 게시물 정보 추출 (좋아요, 댓글, 날짜 등)
Selenium을 사용한 동적 웹 페이지 크롤링
"""
import re
import requests
import json
import time
from typing import Dict, Optional
from datetime import datetime
from utils.logger import safe_log, log_error
import logging
from dotenv import load_dotenv
import os

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    safe_log(logging.WARNING, "Selenium not available. Install selenium and webdriver-manager for better Instagram crawling.")

# 환경 변수 로드
load_dotenv()


class InstagramCrawler:
    """인스타그램 게시물 크롤링 클래스"""
    
    def __init__(self, use_selenium: bool = True):
        """
        Args:
            use_selenium: Selenium 사용 여부 (기본값: True)
        """
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.session = requests.Session()
        # Instagram이 봇을 차단할 수 있으므로 User-Agent 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
        })
        # Instagram Graph API Access Token (선택사항)
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    
    def parse_instagram_url(self, url: str) -> Optional[str]:
        """
        Instagram URL에서 게시물 ID 추출
        
        Args:
            url: Instagram 게시물 URL
            
        Returns:
            게시물 ID 또는 None
        """
        # 다양한 Instagram URL 형식 지원
        patterns = [
            r'instagram\.com/p/([A-Za-z0-9_-]+)',
            r'instagram\.com/reel/([A-Za-z0-9_-]+)',
            r'instagram\.com/tv/([A-Za-z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def validate_url(self, url: str) -> bool:
        """Instagram URL 유효성 검증"""
        if not url:
            return False
        
        # Instagram 도메인 확인
        if 'instagram.com' not in url.lower():
            return False
        
        # 게시물 ID 추출 가능한지 확인
        post_id = self.parse_instagram_url(url)
        return post_id is not None
    
    def get_oembed_data(self, url: str) -> Dict:
        """
        Instagram oEmbed API 사용 (인증 불필요)
        공개 게시물의 기본 정보 제공
        """
        try:
            oembed_url = "https://api.instagram.com/oembed"
            params = {
                'url': url,
                'omitscript': 'true'
            }
            
            response = self.session.get(oembed_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'username': data.get('author_name', '').replace('@', ''),
                'caption': data.get('title', ''),
                'thumbnail_url': data.get('thumbnail_url'),
            }
        except Exception as e:
            log_error(e, f"Error fetching oEmbed data: {url}")
            return {}
    
    def extract_from_html(self, html: str) -> Dict:
        """
        HTML에서 게시물 정보 추출
        Instagram의 JSON 데이터 구조에서 정보 추출
        
        Args:
            html: Instagram 페이지 HTML
            
        Returns:
            추출된 정보 딕셔너리
        """
        data = {
            'like_count': None,
            'comment_count': None,
            'post_date': None,
            'caption': None,
            'username': None,
        }
        
        try:
            # Instagram은 게시물 정보를 여러 형태로 포함시킴
            
            # 패턴 1: JSON 데이터 직접 추출
            # 좋아요 수
            like_patterns = [
                r'"like_count":\s*(\d+)',
                r'"edge_media_preview_like":\s*\{[^}]*"count":\s*(\d+)',
                r'"edge_liked_by":\s*\{[^}]*"count":\s*(\d+)',
            ]
            for pattern in like_patterns:
                match = re.search(pattern, html)
                if match:
                    data['like_count'] = int(match.group(1))
                    break
            
            # 댓글 수
            comment_patterns = [
                r'"comment_count":\s*(\d+)',
                r'"edge_media_to_comment":\s*\{[^}]*"count":\s*(\d+)',
                r'"edge_media_to_parent_comment":\s*\{[^}]*"count":\s*(\d+)',
            ]
            for pattern in comment_patterns:
                match = re.search(pattern, html)
                if match:
                    data['comment_count'] = int(match.group(1))
                    break
            
            # 날짜
            date_patterns = [
                r'"taken_at_timestamp":\s*(\d+)',
                r'"uploadDate":\s*"([^"]+)"',
            ]
            for pattern in date_patterns:
                match = re.search(pattern, html)
                if match:
                    if pattern.startswith('"taken_at_timestamp"'):
                        timestamp = int(match.group(1))
                        data['post_date'] = datetime.fromtimestamp(timestamp).isoformat()
                    else:
                        data['post_date'] = match.group(1)
                    break
            
            # 사용자명
            username_patterns = [
                r'"username":\s*"([^"]+)"',
                r'"owner":\s*\{[^}]*"username":\s*"([^"]+)"',
            ]
            for pattern in username_patterns:
                match = re.search(pattern, html)
                if match:
                    data['username'] = match.group(1)
                    break
            
            # 캡션
            caption_patterns = [
                r'"edge_media_to_caption":\s*\{[^}]*"text":\s*"([^"]+)"',
                r'"caption":\s*"([^"]+)"',
            ]
            for pattern in caption_patterns:
                match = re.search(pattern, html)
                if match:
                    # 이스케이프 문자 처리
                    caption = match.group(1).replace('\\n', '\n').replace('\\"', '"')
                    data['caption'] = caption
                    break
            
            # 패턴 2: window._sharedData에서 추출
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.+?});', html, re.DOTALL)
            if shared_data_match:
                try:
                    shared_data = json.loads(shared_data_match.group(1))
                    # 데이터 구조 탐색
                    if 'entry_data' in shared_data:
                        entry_data = shared_data['entry_data']
                        # 게시물 페이지인 경우
                        if 'PostPage' in entry_data:
                            post_data = entry_data['PostPage'][0]['graphql']['shortcode_media']
                            if not data['like_count']:
                                data['like_count'] = post_data.get('edge_media_preview_like', {}).get('count')
                            if not data['comment_count']:
                                data['comment_count'] = post_data.get('edge_media_to_comment', {}).get('count')
                            if not data['post_date']:
                                timestamp = post_data.get('taken_at_timestamp')
                                if timestamp:
                                    data['post_date'] = datetime.fromtimestamp(timestamp).isoformat()
                            if not data['username']:
                                data['username'] = post_data.get('owner', {}).get('username')
                            if not data['caption']:
                                edges = post_data.get('edge_media_to_caption', {}).get('edges', [])
                                if edges:
                                    data['caption'] = edges[0].get('node', {}).get('text', '')
                except Exception as e:
                    safe_log(logging.DEBUG, f"Could not parse _sharedData: {str(e)}")
            
        except Exception as e:
            log_error(e, "Error extracting data from HTML")
        
        return data
    
    def crawl_with_selenium(self, url: str) -> Dict:
        """
        Selenium을 사용한 Instagram 크롤링
        JavaScript 렌더링이 완료된 후 데이터 추출
        
        Args:
            url: Instagram 게시물 URL
            
        Returns:
            게시물 정보 딕셔너리
        """
        driver = None
        try:
            # Chrome 옵션 설정
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # 헤드리스 모드
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # WebDriver 생성
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 페이지 로드
            driver.get(url)
            
            # 페이지 로딩 대기 (최대 10초)
            wait = WebDriverWait(driver, 10)
            
            # 좋아요 수 추출 시도
            like_count = None
            try:
                # 여러 가능한 선택자 시도
                like_selectors = [
                    "//span[contains(text(), '좋아요')]/following-sibling::span",
                    "//span[contains(text(), 'likes')]/following-sibling::span",
                    "//a[contains(@href, '/liked_by/')]//span",
                    "//span[contains(@class, 'html-span')]",
                ]
                for selector in like_selectors:
                    try:
                        element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                        text = element.text.strip()
                        # 숫자만 추출
                        numbers = re.findall(r'[\d,]+', text.replace(',', ''))
                        if numbers:
                            like_count = int(numbers[0].replace(',', ''))
                            break
                    except:
                        continue
            except Exception as e:
                safe_log(logging.DEBUG, f"Could not extract like count: {str(e)}")
            
            # 댓글 수 추출 시도
            comment_count = None
            try:
                comment_selectors = [
                    "//span[contains(text(), '댓글')]/following-sibling::span",
                    "//span[contains(text(), 'comments')]/following-sibling::span",
                    "//a[contains(@href, '/comments/')]//span",
                ]
                for selector in comment_selectors:
                    try:
                        element = driver.find_element(By.XPATH, selector)
                        text = element.text.strip()
                        numbers = re.findall(r'[\d,]+', text.replace(',', ''))
                        if numbers:
                            comment_count = int(numbers[0].replace(',', ''))
                            break
                    except:
                        continue
            except Exception as e:
                safe_log(logging.DEBUG, f"Could not extract comment count: {str(e)}")
            
            # 사용자명 추출
            username = None
            try:
                username_element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/') and not(contains(@href, 'instagram.com'))]//span")))
                username = username_element.text.strip().replace('@', '')
            except:
                pass
            
            # 캡션 추출
            caption = None
            try:
                caption_element = driver.find_element(By.XPATH, "//h1[contains(@class, '')]//span")
                caption = caption_element.text.strip()
            except:
                pass
            
            # HTML에서 추가 데이터 추출
            html = driver.page_source
            html_data = self.extract_from_html(html)
            
            # 데이터 병합
            data = {
                'url': url,
                'post_id': self.parse_instagram_url(url),
                'username': username or html_data.get('username'),
                'caption': caption or html_data.get('caption'),
                'like_count': like_count or html_data.get('like_count'),
                'comment_count': comment_count or html_data.get('comment_count'),
                'post_date': html_data.get('post_date'),
                'share_count': None,
                'method': 'selenium'
            }
            
            return data
            
        except Exception as e:
            log_error(e, f"Error with Selenium crawling: {url}")
            raise ValueError(f"Selenium crawling failed: {str(e)}")
        finally:
            if driver:
                driver.quit()
    
    def crawl_post(self, url: str) -> Dict:
        """
        Instagram 게시물 정보 크롤링
        Selenium 우선 사용, 실패 시 oEmbed + HTML 파싱
        
        Args:
            url: Instagram 게시물 URL
            
        Returns:
            게시물 정보 딕셔너리
        """
        # URL 검증
        if not self.validate_url(url):
            raise ValueError("Invalid Instagram URL. Please provide a valid Instagram post URL.")
        
        # Selenium 사용 시도
        if self.use_selenium:
            try:
                safe_log(logging.INFO, f"Attempting Selenium crawl for: {url}")
                return self.crawl_with_selenium(url)
            except Exception as e:
                safe_log(logging.WARNING, f"Selenium crawl failed, falling back to requests: {str(e)}")
        
        # 폴백: oEmbed + HTML 파싱
        try:
            # 1단계: oEmbed API로 기본 정보 가져오기
            oembed_data = self.get_oembed_data(url)
            
            # 2단계: HTML에서 상세 정보 추출
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            html = response.text
            
            # HTML에서 데이터 추출
            html_data = self.extract_from_html(html)
            
            # 데이터 병합 (oEmbed 우선, HTML로 보완)
            data = {
                'url': url,
                'post_id': self.parse_instagram_url(url),
                'username': html_data.get('username') or oembed_data.get('username'),
                'caption': html_data.get('caption') or oembed_data.get('caption'),
                'like_count': html_data.get('like_count'),
                'comment_count': html_data.get('comment_count'),
                'post_date': html_data.get('post_date'),
                'share_count': None,  # Instagram은 공유 수를 직접 제공하지 않음
                'thumbnail_url': oembed_data.get('thumbnail_url'),
                'method': 'requests'
            }
            
            # 데이터 추출 성공 여부 확인
            if not any([data['like_count'], data['comment_count'], data['post_date']]):
                safe_log(logging.WARNING, "Could not extract detailed data from Instagram page. Using oEmbed data only.")
            
            return data
            
        except requests.exceptions.RequestException as e:
            log_error(e, f"Error fetching Instagram URL: {url}")
            raise ValueError(f"Failed to fetch Instagram post: {str(e)}")
        except Exception as e:
            log_error(e, f"Error crawling Instagram post: {url}")
            raise ValueError(f"Error crawling Instagram post: {str(e)}")
    


def crawl_instagram_post(url: str, use_selenium: bool = True) -> Dict:
    """
    Instagram 게시물 크롤링 헬퍼 함수
    
    Args:
        url: Instagram 게시물 URL
        use_selenium: Selenium 사용 여부 (기본값: True)
        
    Returns:
        게시물 정보 딕셔너리
    """
    crawler = InstagramCrawler(use_selenium=use_selenium)
    return crawler.crawl_post(url)

