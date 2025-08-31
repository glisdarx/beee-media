#!/bin/bash

# Beee Media 一键Cloudflare部署脚本
echo "🚀 开始部署 Beee Media 到 Cloudflare Pages"

# 设置API令牌
export CLOUDFLARE_API_TOKEN="cd226a2bc1a1ff06d8408b7ef12df5b4"

# 提交最新代码到Git
echo "📦 准备最新代码..."
git add .
git commit -m "🚀 准备Cloudflare部署 - $(date '+%Y-%m-%d %H:%M:%S')" || true
git push origin main

echo "✅ 代码已推送到 GitHub"

# 项目信息
PROJECT_NAME="beee-media"
DOMAIN="beeemedia.com"

echo "📋 部署信息:"
echo "  项目名称: $PROJECT_NAME"
echo "  域名: $DOMAIN"
echo "  GitHub仓库: glisdarx/beee-media"

echo ""
echo "🌟 请按照以下步骤在 Cloudflare Dashboard 中完成部署:"
echo ""
echo "1. 访问 Cloudflare Dashboard: https://dash.cloudflare.com"
echo "2. 登录您的账号"
echo "3. 在左侧菜单选择 'Pages'"
echo "4. 点击 'Create a project'"
echo "5. 选择 'Connect to Git'"
echo "6. 连接 GitHub 并选择仓库: glisdarx/beee-media"
echo "7. 配置构建设置:"
echo "   - Project name: beee-media"
echo "   - Production branch: main"
echo "   - Framework preset: None"
echo "   - Build command: echo 'Static deployment ready'"
echo "   - Build output directory: /"
echo "8. 设置环境变量:"
echo "   - TIKHUB_API_KEY = w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA=="
echo "9. 点击 'Save and Deploy'"
echo "10. 部署完成后，在 'Custom domains' 中添加: beeemedia.com"

echo ""
echo "🎯 预期结果:"
echo "- 主页: https://beeemedia.com"
echo "- 创作者搜索: https://beeemedia.com/creators"
echo "- 完整API功能和搜索功能"

echo ""
echo "📞 如果遇到问题，请检查:"
echo "1. GitHub仓库权限"
echo "2. Cloudflare账号权限"
echo "3. 域名DNS设置"
echo "4. 环境变量配置"

echo ""
echo "🎉 部署脚本准备完成！请在浏览器中完成Cloudflare Pages设置。"
