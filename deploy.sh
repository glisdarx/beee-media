#!/bin/bash

# Beee Media 一键部署脚本
echo "🚀 开始部署 Beee Media 到 beeemedia.com"

# 检查必要的工具
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 未安装，请先安装 $1"
        exit 1
    fi
}

# 检查Git
check_tool git

# 检查是否在项目目录中
if [ ! -f "index.html" ] || [ ! -f "netlify.toml" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 提示用户选择部署方式
echo "请选择部署方式："
echo "1) Netlify (推荐)"
echo "2) Vercel"
echo "3) Cloudflare Pages"
echo "4) 仅准备文件"

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo "🌟 选择了 Netlify 部署"
        DEPLOY_METHOD="netlify"
        ;;
    2)
        echo "⚡ 选择了 Vercel 部署"
        DEPLOY_METHOD="vercel"
        ;;
    3)
        echo "☁️  选择了 Cloudflare Pages 部署"
        DEPLOY_METHOD="cloudflare"
        ;;
    4)
        echo "📁 仅准备部署文件"
        DEPLOY_METHOD="prepare"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

# 检查并初始化Git仓库
if [ ! -d ".git" ]; then
    echo "📝 初始化Git仓库..."
    git init
    echo "node_modules/" > .gitignore
    echo "*.log" >> .gitignore
    echo ".env" >> .gitignore
    echo "debug_api.py" >> .gitignore
    echo "temp_*" >> .gitignore
fi

# 添加所有文件到Git
echo "📦 准备部署文件..."
git add .
git commit -m "🚀 Beee Media 网站部署 - $(date '+%Y-%m-%d %H:%M:%S')" || true

# 根据选择的方法进行部署
case $DEPLOY_METHOD in
    "netlify")
        echo "🌟 部署到 Netlify..."
        
        # 检查是否安装了 Netlify CLI
        if ! command -v netlify &> /dev/null; then
            echo "📦 安装 Netlify CLI..."
            npm install -g netlify-cli
        fi
        
        # 提示用户登录
        echo "🔑 请确保已登录 Netlify..."
        netlify login
        
        # 部署
        echo "🚀 开始部署..."
        netlify deploy --prod --dir . --message "Beee Media Deploy $(date)"
        
        echo "✅ Netlify 部署完成！"
        echo "🌐 请在 Netlify Dashboard 中配置自定义域名 beeemedia.com"
        ;;
        
    "vercel")
        echo "⚡ 部署到 Vercel..."
        
        # 检查是否安装了 Vercel CLI
        if ! command -v vercel &> /dev/null; then
            echo "📦 安装 Vercel CLI..."
            npm install -g vercel
        fi
        
        # 创建 vercel.json 配置
        cat > vercel.json << 'EOF'
{
  "functions": {
    "netlify/functions/creators-search.js": {
      "runtime": "nodejs18.x"
    },
    "netlify/functions/trends.js": {
      "runtime": "nodejs18.x"
    }
  },
  "rewrites": [
    {
      "source": "/api/creators/search",
      "destination": "/netlify/functions/creators-search"
    },
    {
      "source": "/api/trends",
      "destination": "/netlify/functions/trends"
    }
  ]
}
EOF
        
        # 部署
        echo "🚀 开始部署..."
        vercel --prod
        
        echo "✅ Vercel 部署完成！"
        echo "🌐 请在 Vercel Dashboard 中配置自定义域名 beeemedia.com"
        ;;
        
    "cloudflare")
        echo "☁️  准备 Cloudflare Pages 部署..."
        echo "📝 请手动执行以下步骤："
        echo "1. 将代码推送到 GitHub"
        echo "2. 在 Cloudflare Dashboard 中选择 Pages"
        echo "3. 连接您的 GitHub 仓库"
        echo "4. 域名会自动配置为 beeemedia.com"
        ;;
        
    "prepare")
        echo "📁 文件准备完成！"
        ;;
esac

# 显示部署后的检查清单
echo ""
echo "🎉 部署准备完成！"
echo ""
echo "📋 部署后检查清单："
echo "✅ 主页访问: https://beeemedia.com"
echo "✅ 创作者搜索: https://beeemedia.com/creators.html"
echo "✅ SEO验证: 页面标题、描述、图标"
echo "✅ API功能: 创作者搜索是否正常"
echo "✅ 移动端: 响应式设计"
echo "✅ HTTPS: SSL证书"
echo "✅ 速度测试: 页面加载速度"
echo ""
echo "🔧 需要设置的环境变量:"
echo "TIKHUB_API_KEY=w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA=="
echo ""
echo "📖 详细说明请查看: DEPLOYMENT_GUIDE.md"
echo ""
echo "🎯 下一步:"
echo "1. 配置自定义域名 beeemedia.com"
echo "2. 设置环境变量"
echo "3. 测试所有功能"
echo "4. 添加 Google Analytics (可选)"

echo ""
echo "🚀 Beee Media 部署完成！"