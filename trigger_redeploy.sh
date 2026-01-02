#!/bin/bash
# Vercel 자동 재배포 트리거 스크립트

echo "Vercel 자동 재배포를 트리거합니다..."
git commit --allow-empty -m "Trigger Vercel redeploy"
git push

echo ""
echo "✅ GitHub에 푸시 완료!"
echo "Vercel이 자동으로 재배포를 시작합니다."
echo ""
echo "확인 방법:"
echo "1. Vercel Dashboard → 프로젝트 → Deployments 탭"
echo "2. 새로운 배포 항목이 'Building' 상태로 나타나는지 확인"
echo "3. 몇 분 후 'Ready' 상태가 되면 완료"

