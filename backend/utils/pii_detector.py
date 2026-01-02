"""
PII (개인정보) 감지 모듈
정규식을 사용한 1차 분석 (Rule-based)
"""
import re
from typing import List, Dict, Tuple


class PIIDetector:
    """개인정보 감지 클래스"""
    
    def __init__(self):
        # 한국 휴대폰 번호 패턴 (010-1234-5678, 01012345678 등)
        self.phone_patterns = [
            r'010-?\d{4}-?\d{4}',  # 010-1234-5678 또는 01012345678
            r'011-?\d{3,4}-?\d{4}',
            r'016-?\d{3,4}-?\d{4}',
            r'017-?\d{3,4}-?\d{4}',
            r'018-?\d{3,4}-?\d{4}',
            r'019-?\d{3,4}-?\d{4}',
        ]
        
        # 주민등록번호 패턴 (123456-1234567 형식)
        self.ssn_pattern = r'\d{6}-?\d{7}'
        
        # 이메일 패턴
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # 신용카드 번호 패턴 (간단한 패턴)
        self.card_pattern = r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}'
        
        # 계좌번호 패턴 (은행별로 다양하지만 기본 패턴)
        self.account_patterns = [
            r'\d{3,4}-\d{2,3}-\d{6,12}',  # 일반적인 계좌번호 형식
        ]
    
    def detect_phone_numbers(self, text: str) -> List[Dict[str, any]]:
        """휴대폰 번호 감지"""
        findings = []
        for pattern in self.phone_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                findings.append({
                    "type": "phone_number",
                    "value": match.group(),
                    "severity": "high",
                    "position": match.span(),
                    "description": "한국 휴대폰 번호가 감지되었습니다"
                })
        return findings
    
    def detect_ssn(self, text: str) -> List[Dict[str, any]]:
        """주민등록번호 감지"""
        findings = []
        matches = re.finditer(self.ssn_pattern, text)
        for match in matches:
            ssn = match.group().replace('-', '')
            # 간단한 유효성 검사 (주민번호 체크섬은 복잡하므로 기본 패턴만 확인)
            if len(ssn) == 13:
                findings.append({
                    "type": "ssn",
                    "value": match.group(),
                    "severity": "high",
                    "position": match.span(),
                    "description": "주민등록번호 형식이 감지되었습니다"
                })
        return findings
    
    def detect_emails(self, text: str) -> List[Dict[str, any]]:
        """이메일 주소 감지"""
        findings = []
        matches = re.finditer(self.email_pattern, text)
        for match in matches:
            findings.append({
                "type": "email",
                "value": match.group(),
                "severity": "medium",
                "position": match.span(),
                "description": "이메일 주소가 감지되었습니다"
            })
        return findings
    
    def detect_card_numbers(self, text: str) -> List[Dict[str, any]]:
        """신용카드 번호 감지"""
        findings = []
        matches = re.finditer(self.card_pattern, text)
        for match in matches:
            findings.append({
                "type": "card_number",
                "value": match.group(),
                "severity": "high",
                "position": match.span(),
                "description": "신용카드 번호 형식이 감지되었습니다"
            })
        return findings
    
    def detect_all(self, text: str) -> Dict[str, any]:
        """
        모든 PII 패턴을 검사
        
        Returns:
            {
                "pii_findings": [...],
                "summary": {
                    "total_count": int,
                    "high_severity": int,
                    "medium_severity": int,
                    "low_severity": int
                }
            }
        """
        all_findings = []
        
        # 각 타입별로 감지
        all_findings.extend(self.detect_phone_numbers(text))
        all_findings.extend(self.detect_ssn(text))
        all_findings.extend(self.detect_emails(text))
        all_findings.extend(self.detect_card_numbers(text))
        
        # 중복 제거 (같은 위치의 같은 값)
        unique_findings = []
        seen = set()
        for finding in all_findings:
            key = (finding["type"], finding["value"], finding["position"])
            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)
        
        # 심각도별 카운트
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        for finding in unique_findings:
            severity = finding.get("severity", "low")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            "pii_findings": unique_findings,
            "summary": {
                "total_count": len(unique_findings),
                "high_severity": severity_counts["high"],
                "medium_severity": severity_counts["medium"],
                "low_severity": severity_counts["low"]
            }
        }

