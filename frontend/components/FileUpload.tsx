'use client';

import { useCallback, useState } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

export default function FileUpload({ onFileSelect, isUploading }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    const file = files[0];
    
    if (file && isValidFileType(file)) {
      onFileSelect(file);
    } else {
      alert('지원하지 않는 파일 형식입니다. PDF, TXT, DOCX 파일만 업로드 가능합니다.');
    }
  }, [onFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      const file = files[0];
      if (isValidFileType(file)) {
        onFileSelect(file);
      } else {
        alert('지원하지 않는 파일 형식입니다. PDF, TXT, DOCX 파일만 업로드 가능합니다.');
      }
    }
  }, [onFileSelect]);

  const isValidFileType = (file: File): boolean => {
    const allowedTypes = [
      'application/pdf',
      'text/plain',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ];
    return allowedTypes.includes(file.type);
  };

  return (
    <div
      className={`relative w-full rounded-2xl border-2 border-dashed transition-all duration-200 ${
        isDragging
          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
          : 'border-gray-300 bg-gray-50 dark:border-gray-700 dark:bg-gray-800/50'
      } ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        type="file"
        id="file-upload"
        className="hidden"
        accept=".pdf,.txt,.docx"
        onChange={handleFileInput}
        disabled={isUploading}
      />
      
      <label
        htmlFor="file-upload"
        className="flex min-h-[300px] cursor-pointer flex-col items-center justify-center p-8 text-center"
      >
        <div className="mb-4">
          <svg
            className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
            />
          </svg>
        </div>
        
        <p className="mb-2 text-lg font-semibold text-gray-700 dark:text-gray-300">
          {isDragging ? '파일을 여기에 놓으세요' : '파일을 드래그 앤 드롭하거나 클릭하여 선택'}
        </p>
        
        <p className="text-sm text-gray-500 dark:text-gray-400">
          PDF, TXT, DOCX 파일만 지원됩니다 (최대 10MB)
        </p>
        
        {isUploading && (
          <div className="mt-4">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-500 border-r-transparent"></div>
          </div>
        )}
      </label>
    </div>
  );
}

