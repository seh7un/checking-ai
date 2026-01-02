'use client';

import { AnalysisResult as AnalysisResultType } from '@/lib/api';

interface AnalysisResultProps {
  result: AnalysisResultType;
}

export default function AnalysisResult({ result }: AnalysisResultProps) {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300';
      case 'low':
        return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-green-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getRiskLabel = (risk: string) => {
    switch (risk) {
      case 'high':
        return '높음';
      case 'medium':
        return '중간';
      case 'low':
        return '낮음';
      default:
        return '알 수 없음';
    }
  };

  const getRiskPercentage = (risk: string, piiSummary: any, aiRisk: string): number => {
    // 기본 위험도에 따른 퍼센트
    let basePercentage = 0;
    switch (risk) {
      case 'high':
        basePercentage = 85;
        break;
      case 'medium':
        basePercentage = 55;
        break;
      case 'low':
        basePercentage = 20;
        break;
      default:
        basePercentage = 50;
    }

    // PII 감지 결과에 따른 조정
    const piiCount = piiSummary.total_count || 0;
    const highSeverityCount = piiSummary.high_severity || 0;
    const mediumSeverityCount = piiSummary.medium_severity || 0;

    // PII가 많을수록 위험도 증가
    if (highSeverityCount > 0) {
      basePercentage += Math.min(highSeverityCount * 3, 10);
    }
    if (mediumSeverityCount > 0) {
      basePercentage += Math.min(mediumSeverityCount * 2, 5);
    }
    if (piiCount > 0) {
      basePercentage += Math.min(piiCount, 5);
    }

    // AI 분석 결과에 따른 조정
    if (aiRisk === 'high' && risk !== 'high') {
      basePercentage += 10;
    } else if (aiRisk === 'medium' && risk === 'low') {
      basePercentage += 5;
    }

    // 0-100 범위로 제한
    return Math.min(Math.max(Math.round(basePercentage), 0), 100);
  };

  return (
    <div className="space-y-6">
      {/* 전체 위험도 */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-gray-100">
          분석 결과
        </h2>
        <div className="flex items-center gap-6">
          <div className="flex flex-col">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
              전체 위험도
            </span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">
                {getRiskPercentage(
                  result.analysis.risk_level,
                  result.analysis.pii_analysis.summary,
                  result.analysis.ai_analysis.result.risk_level
                )}%
              </span>
              <span
                className={`rounded-full px-3 py-1 text-xs font-semibold ${getRiskColor(
                  result.analysis.risk_level
                )}`}
              >
                {getRiskLabel(result.analysis.risk_level)}
              </span>
            </div>
          </div>
          {/* 위험도 진행 바 */}
          <div className="flex-1">
            <div className="h-3 w-full rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  result.analysis.risk_level === 'high'
                    ? 'bg-red-500'
                    : result.analysis.risk_level === 'medium'
                    ? 'bg-yellow-500'
                    : 'bg-green-500'
                }`}
                style={{
                  width: `${getRiskPercentage(
                    result.analysis.risk_level,
                    result.analysis.pii_analysis.summary,
                    result.analysis.ai_analysis.result.risk_level
                  )}%`,
                }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* PII 분석 결과 */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <h2 className="mb-4 text-xl font-bold text-gray-900 dark:text-gray-100">
          개인정보 감지 결과
        </h2>
        
        <div className="mb-4 grid grid-cols-3 gap-4">
          <div className="rounded-lg bg-gray-50 p-4 dark:bg-gray-700/50">
            <p className="text-sm text-gray-600 dark:text-gray-400">전체 감지</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              {result.analysis.pii_analysis.summary.total_count}
            </p>
          </div>
          <div className="rounded-lg bg-red-50 p-4 dark:bg-red-900/20">
            <p className="text-sm text-red-600 dark:text-red-400">높은 위험</p>
            <p className="text-2xl font-bold text-red-700 dark:text-red-300">
              {result.analysis.pii_analysis.summary.high_severity}
            </p>
          </div>
          <div className="rounded-lg bg-yellow-50 p-4 dark:bg-yellow-900/20">
            <p className="text-sm text-yellow-600 dark:text-yellow-400">중간 위험</p>
            <p className="text-2xl font-bold text-yellow-700 dark:text-yellow-300">
              {result.analysis.pii_analysis.summary.medium_severity}
            </p>
          </div>
        </div>

        {result.analysis.pii_analysis.findings.length > 0 ? (
          <div className="space-y-3">
            {result.analysis.pii_analysis.findings.map((finding, index) => (
              <div
                key={index}
                className="flex items-start gap-3 rounded-lg border border-gray-200 p-4 dark:border-gray-700"
              >
                <div
                  className={`mt-1 h-3 w-3 rounded-full ${getSeverityColor(
                    finding.severity
                  )}`}
                ></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900 dark:text-gray-100">
                      {finding.type === 'phone_number' && '전화번호'}
                      {finding.type === 'ssn' && '주민등록번호'}
                      {finding.type === 'email' && '이메일'}
                      {finding.type === 'card_number' && '신용카드 번호'}
                      {!['phone_number', 'ssn', 'email', 'card_number'].includes(finding.type) && finding.type}
                    </span>
                    <span
                      className={`rounded px-2 py-1 text-xs font-medium ${getRiskColor(
                        finding.severity
                      )}`}
                    >
                      {getRiskLabel(finding.severity)}
                    </span>
                  </div>
                  <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    {finding.description}
                  </p>
                  <p className="mt-1 font-mono text-xs text-gray-500 dark:text-gray-500">
                    {finding.value}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 dark:text-gray-400">
            감지된 개인정보가 없습니다.
          </p>
        )}
      </div>

      {/* AI 분석 결과 */}
      <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-gray-800">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">
            AI 문맥 분석
          </h2>
          <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 dark:bg-gray-700 dark:text-gray-300">
            {result.analysis.ai_analysis.method === 'openai' ? 'OpenAI GPT' : 'Mock 분석'}
          </span>
        </div>

        {result.analysis.ai_analysis.note && (
          <div className="mb-4 rounded-lg bg-yellow-50 p-3 text-sm text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300">
            {result.analysis.ai_analysis.note}
          </div>
        )}

        <div className="space-y-4">
          {result.analysis.ai_analysis.result.issues.map((issue, index) => (
            <div
              key={index}
              className="rounded-lg border border-gray-200 p-4 dark:border-gray-700"
            >
              <div className="flex items-start gap-3">
                <div
                  className={`mt-1 h-3 w-3 rounded-full ${getSeverityColor(
                    issue.severity
                  )}`}
                ></div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900 dark:text-gray-100">
                      {issue.type}
                    </span>
                    <span
                      className={`rounded px-2 py-1 text-xs font-medium ${getRiskColor(
                        issue.severity
                      )}`}
                    >
                      {getRiskLabel(issue.severity)}
                    </span>
                  </div>
                  
                  <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
                    {issue.description}
                  </p>

                  {/* 문제가 되는 텍스트 표시 */}
                  {issue.problematic_text && (
                    <div className="mt-3 rounded-lg border-l-4 border-red-500 bg-red-50 p-3 dark:bg-red-900/10">
                      <p className="mb-1 text-xs font-semibold text-red-700 dark:text-red-400">
                        문제가 되는 텍스트:
                      </p>
                      <p className="font-mono text-sm text-red-900 dark:text-red-300">
                        "{issue.problematic_text}"
                      </p>
                    </div>
                  )}

                  {/* 수정된 텍스트 제안 */}
                  {issue.corrected_text && (
                    <div className="mt-3 rounded-lg border-l-4 border-green-500 bg-green-50 p-3 dark:bg-green-900/10">
                      <p className="mb-1 text-xs font-semibold text-green-700 dark:text-green-400">
                        수정 제안:
                      </p>
                      <p className="font-mono text-sm text-green-900 dark:text-green-300">
                        "{issue.corrected_text}"
                      </p>
                    </div>
                  )}

                  {/* 개선 제안 */}
                  <div className="mt-3 rounded-lg bg-blue-50 p-3 dark:bg-blue-900/10">
                    <p className="mb-1 text-xs font-semibold text-blue-700 dark:text-blue-400">
                      💡 개선 제안:
                    </p>
                    <p className="text-sm text-blue-900 dark:text-blue-300">
                      {issue.suggestion}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 rounded-lg bg-gray-50 p-4 dark:bg-gray-700/50">
          <p className="text-sm text-gray-700 dark:text-gray-300">
            {result.analysis.ai_analysis.result.summary}
          </p>
        </div>
      </div>

      {/* 면책 조항 */}
      <div className="mt-6 rounded-lg border-2 border-yellow-300 bg-yellow-50 p-4 dark:border-yellow-700 dark:bg-yellow-900/20">
        <div className="flex items-start gap-3">
          <svg
            className="mt-0.5 h-5 w-5 flex-shrink-0 text-yellow-600 dark:text-yellow-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <div className="flex-1">
            <h3 className="mb-2 font-semibold text-yellow-900 dark:text-yellow-200">
              ⚠️ 중요 안내
            </h3>
            <p className="text-sm leading-relaxed text-yellow-800 dark:text-yellow-300">
              본 분석 결과는 <strong>참고용</strong>으로 제공되며, 법적 자문을 대체하지 않습니다.
              문서의 개인정보 노출, 계약의 불리한 조항, 법적 위험 요소 등에 대한 분석은 
              <strong> 자동화된 시스템</strong>에 의한 것이며, 실제 법적 검토나 전문가의 의견을 대신할 수 없습니다.
            </p>
            <p className="mt-2 text-sm leading-relaxed text-yellow-800 dark:text-yellow-300">
              <strong>본 서비스는 분석 결과에 대한 법적 책임을 지지 않으며</strong>, 
              중요한 문서의 경우 반드시 법무 전문가의 검토를 받으시기 바랍니다.
              임차인의 권리를 보호하고 법적 분쟁을 예방하기 위해서는 각 조항을 전문가와 함께 재검토하고 수정하는 것이 중요합니다.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

