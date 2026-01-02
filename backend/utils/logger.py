"""
로깅 유틸리티
민감한 정보가 로그에 기록되지 않도록 처리
"""
import logging
import re
from typing import Any

# 로거 설정
logger = logging.getLogger("document_analyzer")
logger.setLevel(logging.INFO)

# 콘솔 핸들러
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# 포맷터 (민감 정보 마스킹)
class SensitiveDataFormatter(logging.Formatter):
    """민감한 정보를 마스킹하는 포맷터"""
    
    # 마스킹할 패턴들
    SENSITIVE_PATTERNS = [
        (r'\b\d{3}-\d{4}-\d{4}\b', 'XXX-XXXX-XXXX'),  # 전화번호
        (r'\b\d{6}-\d{7}\b', 'XXXXXX-XXXXXXX'),  # 주민등록번호
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]'),  # 이메일
        (r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', 'XXXX-XXXX-XXXX-XXXX'),  # 카드번호
        (r'sk-[A-Za-z0-9]+', 'sk-***'),  # API Key
    ]
    
    def format(self, record: logging.LogRecord) -> str:
        """로그 메시지에서 민감 정보 마스킹"""
        original_msg = super().format(record)
        
        # 민감 정보 마스킹
        masked_msg = original_msg
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            masked_msg = re.sub(pattern, replacement, masked_msg)
        
        return masked_msg

formatter = SensitiveDataFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def safe_log(level: int, message: str, *args, **kwargs):
    """
    안전한 로깅 (민감 정보 자동 마스킹)
    
    Args:
        level: 로그 레벨 (logging.INFO, logging.ERROR 등)
        message: 로그 메시지
        *args, **kwargs: 추가 인자
    """
    logger.log(level, message, *args, **kwargs)


def log_error(error: Exception, context: str = ""):
    """
    에러 로깅 (민감 정보 제외)
    
    Args:
        error: 발생한 예외
        context: 에러 발생 컨텍스트
    """
    error_msg = f"{context}: {type(error).__name__}"
    # 에러 메시지에 민감 정보가 포함될 수 있으므로 타입만 로깅
    logger.error(error_msg, exc_info=False)  # exc_info=False로 스택 트레이스 제외


def sanitize_for_logging(data: Any) -> str:
    """
    로깅 전 데이터 정제 (민감 정보 제거)
    
    Args:
        data: 로깅할 데이터
        
    Returns:
        정제된 문자열
    """
    if isinstance(data, str):
        result = data
        for pattern, replacement in SensitiveDataFormatter.SENSITIVE_PATTERNS:
            result = re.sub(pattern, replacement, result)
        return result
    elif isinstance(data, dict):
        # 딕셔너리의 경우 값만 정제
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = sanitize_for_logging(value)
            else:
                sanitized[key] = value
        return str(sanitized)
    else:
        return str(data)

