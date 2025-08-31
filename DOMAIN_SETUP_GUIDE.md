# 🌐 beeemedia.com 域名配置指南

## 🚨 当前状态
- ✅ **Cloudflare Pages**: 部署成功，可通过 https://beee-media.pages.dev 访问
- ❌ **自定义域名**: beeemedia.com 无法访问，需要配置DNS记录

## 🔧 解决方案：手动添加DNS记录

### 步骤1：登录Cloudflare控制台
1. 打开 https://dash.cloudflare.com
2. 登录您的Cloudflare账户
3. 选择 `beeemedia.com` 域名

### 步骤2：配置DNS记录
在DNS管理页面，添加以下记录：

#### 记录1：根域名
```
类型: CNAME
名称: beeemedia.com (或 @)
目标: beee-media.pages.dev
代理状态: 已代理 (橙色云朵)
TTL: 自动
```

#### 记录2：www子域名 (可选)
```
类型: CNAME
名称: www
目标: beee-media.pages.dev
代理状态: 已代理 (橙色云朵)
TTL: 自动
```

### 步骤3：验证Pages项目设置
1. 进入 Cloudflare Pages
2. 选择 `beee-media` 项目
3. 转到 "自定义域" 选项卡
4. 确认 `beeemedia.com` 显示为 "有效"

## ⏰ 生效时间
- **本地DNS**: 2-5分钟
- **全球DNS**: 最多24小时（通常10-30分钟）

## 🧪 测试命令
```bash
# 检查DNS解析
nslookup beeemedia.com

# 检查网站访问
curl -I https://beeemedia.com

# 检查HTTP状态
curl -L https://beeemedia.com
```

## 🎯 预期结果
配置成功后，以下链接应该都能正常访问：
- ✅ https://beeemedia.com
- ✅ https://www.beeemedia.com
- ✅ https://beee-media.pages.dev

## 🔍 故障排除

### 问题1：DNS记录不生效
**症状**: `nslookup beeemedia.com` 返回"No answer"
**解决**: 等待DNS传播，或清除本地DNS缓存
```bash
# macOS
sudo dscacheutil -flushcache

# 检查全球DNS传播
https://www.whatsmydns.net/#CNAME/beeemedia.com
```

### 问题2：SSL证书问题
**症状**: 浏览器显示"不安全连接"
**解决**: Cloudflare会自动配置SSL，等待5-15分钟

### 问题3：Pages项目域名验证失败
**症状**: 自定义域名显示"失败"状态
**解决**: 
1. 确认DNS记录指向正确
2. 在Pages项目中重新验证域名
3. 等待DNS传播完成

## 📞 当前可用访问地址
在DNS生效期间，您可以继续使用：
- **主要地址**: https://beee-media.pages.dev
- **创作者搜索**: https://beee-media.pages.dev/creators

---

**💡 提示**: 如果15分钟后域名仍然无法访问，请检查Cloudflare控制台中的DNS设置是否正确配置。
