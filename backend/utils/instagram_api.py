"""
Instagram Graph API를 사용한 게시물 정보 추출
공개 게시물의 경우 oEmbed API 또는 Graph API 사용
"""
import re
import requests
import json
from typing import Dict, Optional
from datetime import datetime
from utils.logger import safe_log, log_error
import logging


class InstagramAPI:
    """Instagram Graph API를 사용한 게시물 정보 추출 클래스"""
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Args:
            access_token: Instagram Graph API Access Token (선택사항)
                         없으면 oEmbed API 사용
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
    
    def parse_instagram_url(self, url: str) -> Optional[str]:
        """Instagram URL에서 게시물 ID 추출"""
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
        if 'instagram.com' not in url.lower():
            return False
        return self.parse_instagram_url(url) is not None
    
    def get_oembed_data(self, url: str) -> Dict:
        """
        Instagram oEmbed API 사용 (인증 불필요)
        공개 게시물의 기본 정보만 제공
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
                'url': url,
                'post_id': self.parse_instagram_url(url),
                'username': data.get('author_name', '').replace('@', ''),
                'caption': data.get('title', ''),
                'thumbnail_url': data.get('thumbnail_url'),
                # oEmbed는 좋아요/댓글 수를 제공하지 않음
                'like_count': None,
                'comment_count': None,
                'share_count': None,
                'post_date': None,
                'method': 'oembed'
            }
        except Exception as e:
            log_error(e, f"Error fetching oEmbed data: {url}")
            raise ValueError(f"Failed to fetch Instagram oEmbed data: {str(e)}")
    
    def get_graph_api_data(self, url: str) -> Dict:
        """
        Instagram Graph API 사용 (Access Token 필요)
        더 상세한 정보 제공 (좋아요, 댓글 등)
        """
        if not self.access_token:
            raise ValueError("Access Token is required for Graph API")
        
        try:
            # 1단계: URL에서 Media ID 찾기
            # Instagram Graph API는 Media ID가 필요하므로
            # 먼저 oEmbed로 기본 정보를 가져온 후
            # Business Discovery API 또는 다른 방법으로 Media ID 찾기
            
            # 간단한 방법: oEmbed 데이터 먼저 가져오기
            oembed_data = self.get_oembed_data(url)
            
            # 2단계: Graph API로 상세 정보 가져오기
            # 주의: Graph API는 비즈니스/크리에이터 계정이 필요하고
            # 자신의 게시물 또는 연결된 페이지의 게시물만 조회 가능
            
            # 공개 게시물의 경우 Business Discovery API 사용
            # 하지만 이것도 Facebook Page와 연결된 Instagram 비즈니스 계정이 필요
            
            # 대안: HTML에서 데이터 추출 시도
            return self._extract_from_html(url, oembed_data)
            
        except Exception as e:
            log_error(e, f"Error fetching Graph API data: {url}")
            raise ValueError(f"Failed to fetch Instagram Graph API data: {str(e)}")
    
    def _extract_from_html(self, url: str, base_data: Dict) -> Dict:
        """
        HTML에서 추가 데이터 추출 시도
        Instagram의 JSON 데이터 구조에서 정보 추출
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # Instagram은 페이지에 JSON 데이터를 포함시킴
            # window._sharedData 또는 다른 스크립트 태그에서 찾기
            
            # 패턴 1: window._sharedData
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.+?});', html, re.DOTALL)
            if shared_data_match:
                try:
                    shared_data = json.loads(shared_data_match.group(1))
                    # 데이터 구조 탐색
                    if 'entry_data' in shared_data:
                        # 게시물 데이터 추출 시도
                        pass
                except:
                    pass
            
            # 패턴 2: JSON-LD
            json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
            for json_ld in json_ld_matches:
                try:
                    data = json.loads(json_ld)
                    # 필요한 정보 추출
                    if isinstance(data, dict):
                        # 구조에 따라 데이터 추출
                        pass
                except:
                    pass
            
            # 패턴 3: 직접 JSON 데이터 찾기
            # Instagram은 게시물 정보를 JSON으로 포함시킴
            json_patterns = [
                r'"like_count":\s*(\d+)',
                r'"edge_media_preview_like":\s*\{[^}]*"count":\s*(\d+)',
                r'"comment_count":\s*(\d+)',
                r'"edge_media_to_comment":\s*\{[^}]*"count":\s*(\d+)',
                r'"taken_at_timestamp":\s*(\d+)',
            ]
            
            for pattern in json_patterns:
                match = re.search(pattern, html)
                if match:
                    value = match.group(1)
                    if 'like' in pattern.lower():
                        base_data['like_count'] = int(value)
                    elif 'comment' in pattern.lower():
                        base_data['comment_count'] = int(value)
                    elif 'timestamp' in pattern.lower():
                        timestamp = int(value)
                        base_data['post_date'] = datetime.fromtimestamp(timestamp).isoformat()
            
            # 사용자명 추출
            username_match = re.search(r'"username":\s*"([^"]+)"', html)
            if username_match and not base_data.get('username'):
                base_data['username'] = username_match.group(1)
            
            base_data['method'] = 'html_extraction'
            return base_data
            
        except Exception as e:
            log_error(e, f"Error extracting from HTML: {url}")
            return base_data
    
    def get_post_data(self, url: str) -> Dict:
        """
        게시물 데이터 가져오기 (주 메서드)
        Access Token이 있으면 Graph API 사용, 없으면 oEmbed + HTML 추출
        """
        if not self.validate_url(url):
            raise ValueError("Invalid Instagram URL")
        
        try:
            if self.access_token:
                # Graph API 사용 시도
                try:
                    return self.get_graph_api_data(url)
                except:
                    # 실패하면 oEmbed + HTML 추출로 폴백
                    safe_log(logging.WARNING, "Graph API failed, falling back to oEmbed + HTML extraction")
                    oembed_data = self.get_oembed_data(url)
                    return self._extract_from_html(url, oembed_data)
            else:
                # oEmbed + HTML 추출 사용
                oembed_data = self.get_oembed_data(url)
                return self._extract_from_html(url, oembed_data)
                
        except Exception as e:
            log_error(e, f"Error getting post data: {url}")
            raise ValueError(f"Failed to get Instagram post data: {str(e)}")


def get_instagram_post_data(url: str, access_token: Optional[str] = None) -> Dict:
    """
    Instagram 게시물 데이터 가져오기 헬퍼 함수
    
    Args:
        url: Instagram 게시물 URL
        access_token: Instagram Graph API Access Token (선택사항)
        
    Returns:
        게시물 정보 딕셔너리
    """
    api = InstagramAPI(access_token=access_token)
    return api.get_post_data(url)

