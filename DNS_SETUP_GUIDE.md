# 🌐 beeemedia.com DNS 配置指南

## 🚨 当前问题
- ❌ **beeemedia.com**: 没有DNS记录，无法访问
- ❌ **www.beeemedia.com**: 没有DNS记录，无法访问
- ✅ **beee-media.pages.dev**: 正常工作

## 🔧 解决方案：在Cloudflare中添加DNS记录

### 步骤1：登录Cloudflare控制台
1. 访问：https://dash.cloudflare.com
2. 登录您的账户
3. 选择域名：`beeemedia.com`

### 步骤2：进入DNS管理
1. 点击左侧菜单中的 **"DNS"**
2. 您将看到DNS记录管理页面

### 步骤3：添加根域名记录
点击 **"添加记录"** 按钮，填入：

```
类型: CNAME
名称: @ (或者直接写 beeemedia.com)
目标: beee-media.pages.dev
代理状态: 已代理 (橙色云朵图标)
TTL: 自动
```

### 步骤4：添加www子域名记录
再次点击 **"添加记录"**，填入：

```
类型: CNAME
名称: www
目标: beee-media.pages.dev
代理状态: 已代理 (橙色云朵图标)
TTL: 自动
```

### 步骤5：验证Pages项目设置
1. 访问：https://dash.cloudflare.com
2. 进入 **Pages** → **beee-media** 项目
3. 转到 **"自定义域"** 选项卡
4. 确认域名状态为 **"有效"**

## ⏰ 生效时间
- **立即生效**: 在Cloudflare网络内（通常2-5分钟）
- **全球生效**: 最多30分钟

## 🧪 验证步骤

配置完成后，等待5分钟，然后测试：

```bash
# 检查DNS解析
nslookup beeemedia.com
nslookup www.beeemedia.com

# 测试网站访问
curl -I https://beeemedia.com
curl -I https://www.beeemedia.com
```

## 🎯 预期结果
配置成功后，以下链接都应该正常工作：
- ✅ https://beeemedia.com
- ✅ https://www.beeemedia.com
- ✅ https://beee-media.pages.dev

## 📋 DNS记录检查清单

配置完成后，您的DNS记录应该包含：

| 类型 | 名称 | 目标 | 代理 |
|------|------|------|------|
| CNAME | @ (或 beeemedia.com) | beee-media.pages.dev | ✅ |
| CNAME | www | beee-media.pages.dev | ✅ |

## 🆘 故障排除

### 问题1：记录添加后仍无法访问
**解决方案**：
1. 等待5-10分钟让DNS传播
2. 清除浏览器缓存
3. 尝试无痕模式访问

### 问题2：SSL证书错误
**解决方案**：
1. 确保代理状态为"已代理"（橙色云朵）
2. 等待Cloudflare自动生成SSL证书（5-15分钟）

### 问题3：Pages项目域名验证失败
**解决方案**：
1. 先添加DNS记录
2. 然后在Pages项目中添加自定义域名
3. 或者删除后重新添加域名

## 💡 重要提醒
- 确保在Cloudflare控制台中操作，而不是域名注册商
- DNS记录的目标必须是 `beee-media.pages.dev`
- 代理状态必须开启（橙色云朵图标）

---

**配置完成后，您就可以使用 beeemedia.com 访问您的网站了！**
