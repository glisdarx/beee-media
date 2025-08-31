# 🚀 Cloudflare Pages 快速部署指南

由于您的域名 `beeemedia.com` 就在 Cloudflare，我推荐使用 Cloudflare Pages 进行部署，这样可以最快速地让网站上线！

## 🌟 优势

- ✅ 域名已在Cloudflare，配置最简单
- ✅ 全球CDN，访问速度最快
- ✅ 免费SSL证书
- ✅ 强大的安全防护
- ✅ 支持Serverless Functions

## 📋 5分钟快速部署步骤

### 1. 准备GitHub仓库

```bash
# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "🚀 Beee Media 网站部署"

# 推送到GitHub（需要先创建仓库）
git remote add origin https://github.com/YOUR_USERNAME/beee-media.git
git push -u origin main
```

### 2. 在Cloudflare中部署

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com)
2. 在左侧菜单选择 **"Pages"**
3. 点击 **"Create a project"**
4. 选择 **"Connect to Git"**
5. 连接您的GitHub账号
6. 选择刚刚创建的仓库
7. 配置构建设置：
   - **Framework preset**: `None`
   - **Build command**: `echo "Static site ready"`
   - **Build output directory**: `/`
8. 点击 **"Save and Deploy"**

### 3. 配置自定义域名

1. 部署完成后，在Pages项目中点击 **"Custom domains"**
2. 点击 **"Set up a custom domain"**
3. 输入 `beeemedia.com`
4. Cloudflare会自动配置DNS记录
5. 等待几分钟即可生效

### 4. 设置环境变量

1. 在Pages项目中点击 **"Settings"**
2. 选择 **"Environment variables"**
3. 添加变量：
   - **Variable name**: `TIKHUB_API_KEY`
   - **Value**: `w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA==`
4. 点击 **"Save"**

### 5. 重新部署

1. 返回 **"Deployments"** 页面
2. 点击最新部署旁的 **"..."** 菜单
3. 选择 **"Retry deployment"**

## 🎯 完成后验证

访问以下链接确认部署成功：

- ✅ **主页**: https://beeemedia.com
- ✅ **创作者搜索**: https://beeemedia.com/creators.html
- ✅ **API测试**: 在创作者页面搜索关键词测试

## 🔧 故障排除

### 问题1: API调用失败
**解决方案**: 检查环境变量是否正确设置

### 问题2: 域名解析错误
**解决方案**: 等待DNS生效（通常5-10分钟）

### 问题3: 页面404错误
**解决方案**: 检查 `_redirects` 文件是否正确配置

## 🚀 高级配置（可选）

### 启用更多功能

1. **Analytics**: 在Cloudflare中启用Web Analytics
2. **Security**: 启用Bot Fight Mode
3. **Performance**: 启用Auto Minify
4. **Caching**: 配置页面缓存规则

### 自动部署

设置完成后，每次向GitHub推送代码，Cloudflare Pages会自动重新部署！

```bash
# 修改代码后
git add .
git commit -m "更新功能"
git push

# Cloudflare自动检测并重新部署
```

## 🎉 恭喜！

您的网站现在应该已经在 https://beeemedia.com 上线了！

---

💡 **提示**: 如果您遇到任何问题，可以查看 Cloudflare Pages 的部署日志，或者参考完整的 `DEPLOYMENT_GUIDE.md` 文件。
