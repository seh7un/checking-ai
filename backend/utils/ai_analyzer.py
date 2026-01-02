"""
AI 기반 심층 분석 모듈
OpenAI API를 사용한 2차 분석 (문맥 기반)
API Key가 없으면 Mocking 처리
"""
import os
import json
import re
from typing import Dict, Optional
import openai
from openai import OpenAI
from dotenv import load_dotenv
from utils.logger import safe_log, log_error
import logging


class AIAnalyzer:
    """AI 기반 문서 분석 클래스"""
    
    def __init__(self):
        # .env 파일을 다시 로드하여 최신 환경 변수 가져오기
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_mock = self.api_key is None or self.api_key.strip() == "" or self.api_key == "your-openai-api-key-here"
        
        if not self.use_mock:
            try:
                # OpenAI 클라이언트 초기화 (명시적으로 api_key만 전달)
                self.client = OpenAI(api_key=self.api_key.strip())
            except Exception as e:
                # OpenAI 클라이언트 생성 실패 시 Mock 모드로 폴백
                log_error(e, "OpenAI client initialization")
                self.use_mock = True
                self.client = None
        else:
            self.client = None
    
    def analyze_context(self, text: str, pii_summary: Dict) -> Dict[str, any]:
        """
        문맥 기반 심층 분석
        
        Args:
            text: 분석할 텍스트
            pii_summary: 1차 PII 분석 결과 요약
            
        Returns:
            AI 분석 결과
        """
        if self.use_mock:
            return self._mock_analysis(text, pii_summary)
        
        return self._openai_analysis(text, pii_summary)
    
    def _openai_analysis(self, text: str, pii_summary: Dict) -> Dict[str, any]:
        """OpenAI API를 사용한 실제 분석"""
        try:
            # 텍스트가 너무 길면 앞부분만 사용 (토큰 제한 고려)
            max_chars = 8000  # 안전한 토큰 수를 위한 문자 제한
            text_to_analyze = text[:max_chars] if len(text) > max_chars else text
            
            prompt = f"""다음 문서를 매우 예민하게 분석하여 문제가 될 수 있는 모든 요소를 찾아주세요.

분석해야 할 항목:
1. 공격적이거나 비방하는 표현
2. 법적 위험 요소 (명예훼손, 모욕, 차별적 표현 등)
3. 비밀 유지 위반 가능성 (기밀 정보, 내부 정보 노출)
4. 개인정보 노출 위험
5. 기타 윤리적/법적 문제가 될 수 있는 내용

이미 감지된 개인정보: {pii_summary.get('total_count', 0)}건

문서 내용:
{text_to_analyze}

중요: 반드시 순수 JSON 형식으로만 응답하세요. 마크다운 코드 블록이나 추가 설명 없이 JSON만 반환하세요.

다음 JSON 형식으로 응답:
{{
    "risk_level": "high|medium|low",
    "issues": [
        {{
            "type": "issue_type",
            "severity": "high|medium|low",
            "description": "문제 설명",
            "problematic_text": "문제가 되는 정확한 텍스트 부분 (원문 그대로)",
            "corrected_text": "수정된 텍스트 제안",
            "suggestion": "구체적인 개선 제안 및 수정 이유"
        }}
    ],
    "summary": "전체 요약"
}}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # 비용 효율적인 모델 사용
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 문서의 법적, 윤리적 위험 요소를 분석하는 전문가입니다. 매우 예민하게 모든 문제를 찾아내세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # 일관된 분석을 위해 낮은 temperature
                max_tokens=2000  # 더 상세한 응답을 위해 토큰 수 증가
            )
            
            # 응답 파싱 (마크다운 코드 블록 제거 및 JSON 추출)
            content = response.choices[0].message.content
            
            # JSON 파싱 시도
            result = None
            json_content = content
            
            # 마크다운 코드 블록 제거 (```json ... ``` 또는 ``` ... ```)
            # 여러 패턴 시도
            json_content = content.strip()
            
            # 패턴 1: ```json ... ``` 형식
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                # 패턴 2: ``` ... ``` 형식 (json 태그 없음)
                json_match = re.search(r'```\s*(\{.*?\})\s*```', content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                else:
                    # 패턴 3: 중괄호로 시작하고 끝나는 JSON 부분만 추출
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(0)
            
            try:
                result = json.loads(json_content)
                # 필수 필드가 없는 경우 기본값 추가
                for issue in result.get("issues", []):
                    if "problematic_text" not in issue:
                        issue["problematic_text"] = None
                    if "corrected_text" not in issue:
                        issue["corrected_text"] = None
            except json.JSONDecodeError as e:
                # JSON 파싱 실패 시 재시도 (더 공격적인 추출)
                try:
                    # 중괄호로 시작하고 끝나는 부분만 추출
                    start_idx = json_content.find('{')
                    end_idx = json_content.rfind('}')
                    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                        json_content_clean = json_content[start_idx:end_idx+1]
                        result = json.loads(json_content_clean)
                        # 필수 필드 추가
                        for issue in result.get("issues", []):
                            if "problematic_text" not in issue:
                                issue["problematic_text"] = None
                            if "corrected_text" not in issue:
                                issue["corrected_text"] = None
                except Exception as parse_error:
                    # 최종 실패 시 텍스트 기반 응답
                    log_error(parse_error, "JSON parsing (final attempt)")
                    safe_log(logging.WARNING, f"Failed to parse AI response. Content length: {len(content)}")
                    result = {
                        "risk_level": "medium",
                        "issues": [
                            {
                                "type": "ai_analysis",
                                "severity": "medium",
                                "description": "AI 분석 결과를 파싱하는 중 오류가 발생했습니다.",
                                "problematic_text": None,
                                "corrected_text": None,
                                "suggestion": "문서를 다시 분석하거나 관리자에게 문의하세요."
                            }
                        ],
                        "summary": "JSON 파싱 오류로 인해 상세 분석 결과를 표시할 수 없습니다."
                    }
            
            return {
                "method": "openai",
                "model": "gpt-4o-mini",
                "result": result
            }
            
        except Exception as e:
            # API 호출 실패 시 Mock으로 폴백
            return self._mock_analysis(text, pii_summary)
    
    def _mock_analysis(self, text: str, pii_summary: Dict) -> Dict[str, any]:
        """Mock 분석 (API Key가 없을 때)"""
        # 텍스트 길이와 PII 감지 결과를 기반으로 간단한 분석
        text_length = len(text)
        pii_count = pii_summary.get('total_count', 0)
        high_severity_count = pii_summary.get('high_severity', 0)
        
        # 위험도 결정 로직
        if high_severity_count > 0:
            risk_level = "high"
        elif pii_count > 0:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # 텍스트 내용 기반 간단한 키워드 검사
        risk_keywords = ["비밀", "기밀", "내부", "공개금지", "유출", "누설"]
        sensitive_keywords = ["법적", "소송", "위험", "문제"]
        
        issues = []
        
        # 키워드 기반 이슈 감지
        text_lower = text.lower()
        for keyword in risk_keywords:
            if keyword in text_lower:
                # 키워드 주변 텍스트 찾기
                keyword_index = text_lower.find(keyword)
                start = max(0, keyword_index - 30)
                end = min(len(text), keyword_index + len(keyword) + 30)
                problematic_text = text[start:end].strip()
                
                issues.append({
                    "type": "sensitive_keyword",
                    "severity": "high",
                    "description": f"'{keyword}' 관련 표현이 발견되었습니다. 기밀 정보 노출 위험이 있을 수 있습니다.",
                    "problematic_text": problematic_text,
                    "corrected_text": f"[기밀 정보 관련 내용 삭제 또는 일반화 필요]",
                    "suggestion": "해당 내용의 공개 가능 여부를 확인하고, 필요시 기밀 정보를 삭제하거나 일반화하세요."
                })
                break
        
        for keyword in sensitive_keywords:
            if keyword in text_lower:
                keyword_index = text_lower.find(keyword)
                start = max(0, keyword_index - 30)
                end = min(len(text), keyword_index + len(keyword) + 30)
                problematic_text = text[start:end].strip()
                
                issues.append({
                    "type": "legal_keyword",
                    "severity": "medium",
                    "description": f"'{keyword}' 관련 표현이 발견되었습니다. 법적 검토가 필요할 수 있습니다.",
                    "problematic_text": problematic_text,
                    "corrected_text": f"[법적 검토 후 수정 필요]",
                    "suggestion": "법무팀과 상의하여 검토하세요."
                })
                break
        
        # PII가 감지된 경우
        if pii_count > 0:
            issues.append({
                "type": "pii_detected",
                "severity": "high" if high_severity_count > 0 else "medium",
                "description": f"{pii_count}건의 개인정보가 감지되었습니다.",
                "problematic_text": None,  # PII는 이미 pii_analysis에서 상세히 표시됨
                "corrected_text": "[개인정보 마스킹 또는 삭제 필요]",
                "suggestion": "개인정보 보호법에 따라 해당 정보의 공개 여부를 신중히 검토하고, 필요시 마스킹 처리하거나 삭제하세요."
            })
        
        return {
            "method": "mock",
            "note": "OpenAI API Key가 설정되지 않아 Mock 분석을 수행했습니다. 실제 분석을 원하시면 OPENAI_API_KEY 환경변수를 설정하세요.",
            "result": {
                "risk_level": risk_level,
                "issues": issues if issues else [
                    {
                        "type": "general",
                        "severity": "low",
                        "description": "명확한 위험 요소가 감지되지 않았습니다.",
                        "problematic_text": None,
                        "corrected_text": None,
                        "suggestion": "문서를 공개하기 전에 최종 검토를 권장합니다."
                    }
                ],
                "summary": f"문서 길이: {text_length}자, 감지된 개인정보: {pii_count}건. {'높은 위험도' if risk_level == 'high' else '중간 위험도' if risk_level == 'medium' else '낮은 위험도'}로 평가됩니다."
            }
        }

