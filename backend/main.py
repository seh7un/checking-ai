"""
Stateless Sensitive Document Analyzer - Backend
FastAPI 서버: 메모리 기반 파일 처리 (Zero Storage Policy)
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn
from dotenv import load_dotenv
import os
import traceback
import logging

# .env 파일에서 환경 변수 로드
load_dotenv()

# 분석 모듈 import
from utils.text_extractor import extract_text_from_memory
from utils.pii_detector import PIIDetector
from utils.ai_analyzer import AIAnalyzer
from utils.logger import safe_log, log_error, sanitize_for_logging

app = FastAPI(
    title="Stateless Document Analyzer API",
    description="Zero-storage document analysis service",
    version="1.0.0"
)

# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 핸들러 - 민감 정보 노출 방지"""
    log_error(exc, f"Unhandled exception in {request.url.path}")
    
    # 클라이언트에는 일반적인 에러 메시지만 반환
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An internal error occurred. Please try again later.",
            "error_type": "InternalServerError"
        }
    )

# CORS 설정: 프론트엔드 접근 허용
# 프로덕션 배포 시 실제 프론트엔드 URL을 추가하세요
FRONTEND_URLS = [
    "http://localhost:3000",  # 개발 환경
    # "https://your-project.vercel.app",  # 프로덕션: 실제 프론트엔드 URL로 변경
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Stateless Document Analyzer API is running",
        "policy": "Zero Storage - All files processed in memory only"
    }


@app.post("/api/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    문서 분석 엔드포인트
    
    핵심 원칙:
    - 파일을 디스크에 저장하지 않음
    - 메모리(RAM)에서만 처리
    - 분석 완료 후 즉시 데이터 휘발
    """
    # 파일명 검증 (보안)
    if file.filename:
        # 파일명에 위험한 문자 제거
        dangerous_chars = ['..', '/', '\\', '\x00']
        if any(char in file.filename for char in dangerous_chars):
            safe_log(logging.WARNING, f"Potentially dangerous filename detected: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="Invalid filename. Please use a safe filename."
            )
    
    # 허용된 파일 타입 검증
    allowed_types = ["application/pdf", "text/plain", 
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    if not file.content_type or file.content_type not in allowed_types:
        safe_log(logging.WARNING, f"Unsupported file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed types: PDF, TXT, DOCX"
        )
    
    try:
        # 메모리에서 파일 읽기 (디스크에 저장하지 않음)
        file_content = await file.read()
        
        # 파일 크기 제한 (예: 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(file_content) > max_size:
            safe_log(logging.WARNING, f"File size exceeds limit: {len(file_content)} bytes")
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {max_size / (1024*1024)}MB"
            )
        
        # 빈 파일 검증
        if len(file_content) == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty. Please upload a file with content."
            )
        
        # 파일 정보 (메타데이터만, 민감 정보 제외)
        file_info = {
            "filename": file.filename or "unknown",
            "content_type": file.content_type,
            "size_bytes": len(file_content)
        }
        
        safe_log(logging.INFO, f"File received: {file_info['filename']}, size: {file_info['size_bytes']} bytes")
        
        # Step 2: 텍스트 추출 및 분석 로직
        try:
            # 1. 텍스트 추출 (메모리에서)
            extracted_text = extract_text_from_memory(file_content, file.content_type)
            
            # 메모리에서 원본 파일 데이터 제거 (텍스트만 유지)
            del file_content
            
            # 2. 1차 분석: PII 감지 (Rule-based)
            pii_detector = PIIDetector()
            pii_result = pii_detector.detect_all(extracted_text)
            
            # 3. 2차 분석: AI 기반 문맥 분석
            ai_analyzer = AIAnalyzer()
            ai_result = ai_analyzer.analyze_context(extracted_text, pii_result["summary"])
            
            # 최종 위험도 결정 (PII와 AI 분석 결과 종합)
            final_risk_level = "low"
            if pii_result["summary"]["high_severity"] > 0:
                final_risk_level = "high"
            elif ai_result["result"]["risk_level"] == "high":
                final_risk_level = "high"
            elif pii_result["summary"]["total_count"] > 0 or ai_result["result"]["risk_level"] == "medium":
                final_risk_level = "medium"
            
            # 메모리에서 추출된 텍스트도 제거
            del extracted_text
            
            return {
                "status": "success",
                "message": "File analyzed in memory (not stored on disk)",
                "file_info": file_info,
                "analysis": {
                    "risk_level": final_risk_level,
                    "pii_analysis": {
                        "findings": pii_result["pii_findings"],
                        "summary": pii_result["summary"]
                    },
                    "ai_analysis": ai_result,
                    "storage_policy": "Zero Storage - All data processed in memory only and immediately discarded",
                    "disclaimer": "본 분석 결과는 참고용으로 제공되며, 법적 자문을 대체하지 않습니다. 자동화된 시스템에 의한 분석으로, 실제 법적 검토나 전문가의 의견을 대신할 수 없습니다. 본 서비스는 분석 결과에 대한 법적 책임을 지지 않으며, 중요한 문서의 경우 반드시 법무 전문가의 검토를 받으시기 바랍니다."
                }
            }
            
        except ValueError as ve:
            # 텍스트 추출 실패
            log_error(ve, "Text extraction failed")
            raise HTTPException(
                status_code=400,
                detail="Failed to extract text from file. Please ensure the file is not corrupted."
            )
        except Exception as analysis_error:
            # 분석 중 오류 발생
            # 보안: 상세한 에러 정보는 로그에만 기록
            log_error(analysis_error, "Analysis error")
            raise HTTPException(
                status_code=500,
                detail="An error occurred during analysis. Please try again."
            )
        
    except HTTPException:
        raise
    except Exception as e:
        # 보안: 상세한 에러 정보는 로그에만 기록 (클라이언트에는 일반적인 메시지만)
        log_error(e, "File processing error")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the file. Please try again."
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

