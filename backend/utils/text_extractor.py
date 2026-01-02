"""
텍스트 추출 유틸리티
메모리 상의 파일 객체에서 텍스트를 추출 (Zero Storage Policy)
"""
import io
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_memory(file_content: bytes, content_type: str) -> str:
    """
    메모리 상의 파일 바이트에서 텍스트를 추출
    
    Args:
        file_content: 파일의 바이트 데이터
        content_type: 파일의 MIME 타입
        
    Returns:
        추출된 텍스트 문자열
        
    Raises:
        ValueError: 지원하지 않는 파일 타입이거나 추출 실패
    """
    try:
        if content_type == "text/plain":
            # TXT 파일: UTF-8로 디코딩
            text = file_content.decode('utf-8')
            
        elif content_type == "application/pdf":
            # PDF 파일: PyPDF2로 추출
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PdfReader(pdf_file)
            text_parts = []
            
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
            
            text = "\n".join(text_parts)
            
        elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # DOCX 파일: python-docx로 추출
            docx_file = io.BytesIO(file_content)
            doc = Document(docx_file)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                text_parts.append(paragraph.text)
            
            text = "\n".join(text_parts)
            
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        return text.strip()
        
    except UnicodeDecodeError:
        # UTF-8 디코딩 실패 시 다른 인코딩 시도
        try:
            if content_type == "text/plain":
                text = file_content.decode('cp949')  # 한글 인코딩
                return text.strip()
        except:
            pass
        raise ValueError("Failed to decode text file. Unsupported encoding.")
    
    except Exception as e:
        raise ValueError(f"Failed to extract text: {str(e)}")

