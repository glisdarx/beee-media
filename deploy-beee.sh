#!/bin/bash

# Beee Media 部署脚本
# 专门为 beeemedia.com 域名设计的部署包

echo "🐝 Beee Media 部署脚本启动..."
echo "=================================="

# 检查必要文件
echo "📋 检查项目文件..."
required_files=("index.html" "styles.css" "script.js" "app.py" "config.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
        exit 1
    fi
done

# 创建部署包
echo "📦 创建Beee Media部署包..."
deploy_dir="deploy-beee"
rm -rf "$deploy_dir"
mkdir -p "$deploy_dir"

# 复制前端文件
echo "📁 复制前端文件..."
cp index.html "$deploy_dir/"
cp styles.css "$deploy_dir/"
cp script.js "$deploy_dir/"
cp README.md "$deploy_dir/"
cp DEPLOYMENT.md "$deploy_dir/"

# 创建Cloudflare Pages配置文件
echo "⚙️ 创建Cloudflare Pages配置..."
cat > "$deploy_dir/_headers" << EOF
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self';
EOF

# 创建Cloudflare Pages重定向规则
cat > "$deploy_dir/_redirects" << EOF
/*      /index.html  200
EOF

# 创建Beee Media专用部署说明
echo "📝 创建Beee Media部署说明..."
cat > "$deploy_dir/BEEE_DEPLOY_INSTRUCTIONS.md" << 'EOF'
# 🐝 Beee Media 部署指南

## 🚀 快速部署到 beeemedia.com

### 1. 登录Cloudflare
访问 [Cloudflare Dashboard](https://dash.cloudflare.com/) 并登录你的账户

### 2. 创建Pages项目
1. 点击左侧菜单的 **"Pages"**
2. 点击 **"Create a project"**
3. 选择 **"Upload assets"**

### 3. 上传文件
1. 将 `beee-media-deploy.zip` 文件拖拽到上传区域
2. 等待文件上传完成
3. 点击 **"Deploy site"**

### 4. 配置域名
1. 部署完成后，点击 **"Custom domains"**
2. 点击 **"Set up a custom domain"**
3. 输入 `beeemedia.com`
4. 按照提示配置DNS记录

## 🌐 域名配置详情

### DNS记录设置
Cloudflare会自动为你配置以下记录：
- **A记录**: `@` → Cloudflare Pages IP
- **CNAME记录**: `www` → `beeemedia.com`

### SSL设置
- **加密模式**: Full (strict)
- **HTTPS重定向**: 自动启用
- **SSL证书**: 自动生成

## 🎨 网站特性

### 设计风格
- 🎯 清新蜜黄主色调，体现蜜蜂精神
- 🌈 现代化渐变和动效
- 📱 完全响应式设计
- ⚡ 高性能加载速度

### 核心功能
- 🌍 AI驱动的增长工作室
- 📊 趋势捕捉与数据分析
- 🎬 AI内容生成
- 🎯 效果预测与分发
- 💰 透明定价方案

## 🔧 部署后配置

### 性能优化
- ✅ 自动CDN加速
- ✅ 图片优化
- ✅ 代码压缩
- ✅ 浏览器缓存

### 安全设置
- ✅ 自动HTTPS
- ✅ 安全头配置
- ✅ 内容安全策略

## 📞 技术支持

如有问题，请：
1. 查看部署日志
2. 检查DNS配置
3. 验证SSL证书状态
4. 联系技术支持

## 🎯 预期结果

部署成功后，你将获得：
- 🐝 专业的企业级网站
- 🌍 全球CDN加速
- 🔒 自动SSL证书
- 📱 完全响应式设计
- ⚡ 高性能加载速度

---

**Beee Media** - 像蜜蜂一样精准、高效、协作！ 🐝✨
EOF

# 创建ZIP包
echo "🗜️ 创建ZIP包..."
cd "$deploy_dir"
zip -r ../beee-media-deploy.zip . -x "*.DS_Store" "*/__pycache__/*"
cd ..

echo "✅ Beee Media部署包创建完成！"
echo "📦 文件: beeee-media-deploy.zip"
echo ""
echo "🎯 下一步："
echo "1. 访问 https://dash.cloudflare.com/pages"
echo "2. 创建新项目"
echo "3. 上传 beeee-media-deploy.zip 文件"
echo "4. 配置 beeemedia.com 域名"
echo ""
echo "🐝 你的Beee Media网站将在几分钟内上线！"
echo ""
echo "✨ 特色功能："
echo "   - 清新蜜黄配色方案"
echo "   - 蜜蜂主题设计元素"
echo "   - AI助手悬浮按钮"
echo "   - 现代化动效和交互"
echo "   - 完全响应式设计"
