#!/bin/bash

# Beee Media 完整版部署脚本
# 包含创作者搜索功能的完整部署包

echo "🐝 Beee Media 完整版部署脚本启动..."
echo "======================================"

# 检查必要文件
echo "📋 检查项目文件..."
required_files=("index.html" "creators.html" "styles.css" "creators-styles.css" "script.js" "creators.js" "app.py" "config.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file 存在"
    else
        echo "❌ $file 缺失"
        exit 1
    fi
done

# 创建部署包
echo "📦 创建Beee Media完整版部署包..."
deploy_dir="deploy-beee-complete"
rm -rf "$deploy_dir"
mkdir -p "$deploy_dir"

# 复制前端文件
echo "📁 复制前端文件..."
cp index.html "$deploy_dir/"
cp creators.html "$deploy_dir/"
cp styles.css "$deploy_dir/"
cp creators-styles.css "$deploy_dir/"
cp script.js "$deploy_dir/"
cp creators.js "$deploy_dir/"
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

# 创建Beee Media完整版部署说明
echo "📝 创建Beee Media完整版部署说明..."
cat > "$deploy_dir/BEEE_COMPLETE_DEPLOY_INSTRUCTIONS.md" << 'EOF'
# 🐝 Beee Media 完整版部署指南

## 🚀 快速部署到 beeemedia.com

### 1. 登录Cloudflare
访问 [Cloudflare Dashboard](https://dash.cloudflare.com/) 并登录你的账户

### 2. 创建Pages项目
1. 点击左侧菜单的 **"Pages"**
2. 点击 **"Create a project"**
3. 选择 **"Upload assets"**

### 3. 上传文件
1. 将 `beee-media-complete-deploy.zip` 文件拖拽到上传区域
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
- 🔍 **创作者搜索功能** (新增)
- 💰 透明定价方案

## 🔍 创作者搜索功能

### 主要特性
- **关键词搜索**: 通过视频关键词精准找到创作者
- **多维度筛选**: 国家、粉丝数、语言、视频数量等
- **详细数据展示**: 包含所有要求的字段信息
- **智能排序**: 支持多种排序方式
- **数据导出**: CSV格式导出搜索结果
- **详情查看**: 模态框展示完整创作者信息

### 数据字段
- 搜索关键词、昵称、唯一ID
- 粉丝数、视频总数、总点赞数
- TikTok账户链接、个人简介
- 最新5个视频链接和播放量
- 平均播放量、中位数播放量
- 预期价格、邮箱地址等

### 用户体验
- **直观界面**: 清晰的搜索表单和结果展示
- **快速响应**: 实时搜索和筛选
- **移动适配**: 完全响应式设计
- **交互友好**: 悬浮效果、加载动画

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
- 🔍 完整的创作者搜索功能

## 📱 页面结构

### 主页 (index.html)
- Hero区域：AI驱动的增长工作室介绍
- 功能展示：三大核心功能
- 产品介绍：趋势雷达、内容生成器、效果预测
- 解决方案：针对不同行业的定制方案
- 定价方案：三个套餐选择
- 联系我们：完整的联系信息

### 创作者搜索页 (creators.html)
- 页面头部：搜索功能介绍和统计数据
- 搜索区域：高级搜索表单和筛选条件
- 结果展示：表格形式展示创作者数据
- 详情模态框：完整的创作者信息展示
- 分页功能：支持大量数据的分页浏览

---

**Beee Media** - 像蜜蜂一样精准、高效、协作！ 🐝✨
EOF

# 创建ZIP包
echo "🗜️ 创建ZIP包..."
cd "$deploy_dir"
zip -r ../beee-media-complete-deploy.zip . -x "*.DS_Store" "*/__pycache__/*"
cd ..

echo "✅ Beee Media完整版部署包创建完成！"
echo "📦 文件: beee-media-complete-deploy.zip"
echo ""
echo "🎯 下一步："
echo "1. 访问 https://dash.cloudflare.com/pages"
echo "2. 创建新项目"
echo "3. 上传 beeee-media-complete-deploy.zip 文件"
echo "4. 配置 beeemedia.com 域名"
echo ""
echo "🐝 你的Beee Media完整版网站将在几分钟内上线！"
echo ""
echo "✨ 完整功能："
echo "   - 清新蜜黄配色方案"
echo "   - 蜜蜂主题设计元素"
echo "   - AI助手悬浮按钮"
echo "   - 现代化动效和交互"
echo "   - 完全响应式设计"
echo "   - 🔍 创作者搜索功能"
echo "   - 📊 详细数据展示"
echo "   - 📤 数据导出功能"
echo "   - 🎯 多维度筛选"
echo "   - 📱 移动端优化"
