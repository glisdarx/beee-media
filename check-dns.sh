#!/bin/bash

echo "🔍 检查 beeemedia.com DNS 配置状态"
echo "================================="

# 检查根域名
echo ""
echo "🔗 检查根域名: beeemedia.com"
nslookup beeemedia.com | grep -E "(NXDOMAIN|answer|Address)" || echo "❌ 没有找到DNS记录"

# 检查www子域名
echo ""
echo "🔗 检查www子域名: www.beeemedia.com"  
nslookup www.beeemedia.com | grep -E "(NXDOMAIN|answer|Address)" || echo "❌ 没有找到DNS记录"

# 检查Pages域名（对比）
echo ""
echo "✅ 对比：正常工作的域名"
nslookup beee-media.pages.dev | grep -E "(answer|Address)" | head -2

echo ""
echo "📋 需要在Cloudflare DNS中添加的记录："
echo "-----------------------------------"
echo "类型: CNAME | 名称: @           | 目标: beee-media.pages.dev"
echo "类型: CNAME | 名称: www         | 目标: beee-media.pages.dev"
echo ""
echo "🌐 配置指南: 查看 DNS_SETUP_GUIDE.md"
