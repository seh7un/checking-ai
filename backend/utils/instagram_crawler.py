"""
인스타그램 크롤링 모듈
Instagram 게시물 정보 추출 (좋아요, 댓글, 날짜 등)
"""
import re
import requests
from typing import Dict, Optional
from datetime import datetime
from utils.logger import safe_log, log_error
import logging


class InstagramCrawler:
    """인스타그램 게시물 크롤링 클래스"""
    
    def __init__(self):
        self.session = requests.Session()
        # Instagram이 봇을 차단할 수 있으므로 User-Agent 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
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
    
    def extract_from_meta_tags(self, html: str) -> Dict:
        """
        HTML의 meta 태그에서 정보 추출
        
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
            # Open Graph 및 Twitter Card meta 태그에서 정보 추출
            # Instagram은 JavaScript로 동적 로딩하므로 meta 태그가 제한적일 수 있음
            
            # 좋아요 수 (meta property="og:description" 또는 다른 태그)
            like_match = re.search(r'"like_count":\s*(\d+)', html)
            if like_match:
                data['like_count'] = int(like_match.group(1))
            
            # 댓글 수
            comment_match = re.search(r'"comment_count":\s*(\d+)', html)
            if comment_match:
                data['comment_count'] = int(comment_match.group(1))
            
            # 날짜
            date_match = re.search(r'"taken_at_timestamp":\s*(\d+)', html)
            if date_match:
                timestamp = int(date_match.group(1))
                data['post_date'] = datetime.fromtimestamp(timestamp).isoformat()
            
            # 사용자명
            username_match = re.search(r'"username":\s*"([^"]+)"', html)
            if username_match:
                data['username'] = username_match.group(1)
            
            # 캡션
            caption_match = re.search(r'"edge_media_to_caption":\s*\{[^}]*"text":\s*"([^"]+)"', html)
            if caption_match:
                data['caption'] = caption_match.group(1)
            
        except Exception as e:
            log_error(e, "Error extracting data from meta tags")
        
        return data
    
    def crawl_post(self, url: str) -> Dict:
        """
        Instagram 게시물 정보 크롤링
        
        Args:
            url: Instagram 게시물 URL
            
        Returns:
            게시물 정보 딕셔너리
        """
        # URL 검증
        if not self.validate_url(url):
            raise ValueError("Invalid Instagram URL. Please provide a valid Instagram post URL.")
        
        try:
            # Instagram 페이지 요청
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # HTML에서 데이터 추출
            data = self.extract_from_meta_tags(html)
            
            # 게시물 ID 추가
            post_id = self.parse_instagram_url(url)
            data['post_id'] = post_id
            data['url'] = url
            
            # 데이터가 없으면 경고
            if not any([data['like_count'], data['comment_count'], data['post_date']]):
                safe_log(logging.WARNING, "Could not extract data from Instagram page. Instagram may have changed their structure.")
                # 대안: JSON-LD 스키마에서 추출 시도
                data = self.extract_from_json_ld(html, data)
            
            return data
            
        except requests.exceptions.RequestException as e:
            log_error(e, f"Error fetching Instagram URL: {url}")
            raise ValueError(f"Failed to fetch Instagram post: {str(e)}")
        except Exception as e:
            log_error(e, f"Error crawling Instagram post: {url}")
            raise ValueError(f"Error crawling Instagram post: {str(e)}")
    
    def extract_from_json_ld(self, html: str, existing_data: Dict) -> Dict:
        """
        JSON-LD 스키마에서 정보 추출 (대안 방법)
        
        Args:
            html: HTML 내용
            existing_data: 기존 데이터
            
        Returns:
            업데이트된 데이터
        """
        try:
            # JSON-LD 스키마 찾기
            json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
            if json_ld_match:
                import json
                json_data = json.loads(json_ld_match.group(1))
                # JSON-LD에서 필요한 정보 추출
                # (Instagram의 실제 구조에 따라 다를 수 있음)
                pass
        except Exception as e:
            log_error(e, "Error extracting from JSON-LD")
        
        return existing_data


def crawl_instagram_post(url: str) -> Dict:
    """
    Instagram 게시물 크롤링 헬퍼 함수
    
    Args:
        url: Instagram 게시물 URL
        
    Returns:
        게시물 정보 딕셔너리
    """
    crawler = InstagramCrawler()
    return crawler.crawl_post(url)

