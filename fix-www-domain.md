# 🔧 修复 www.beeemedia.com 访问问题

## 🚨 当前状态
- ✅ **beeemedia.com**: 正常工作 (HTTP 200)
- ❌ **www.beeemedia.com**: HTTP 522 错误 (连接超时)

## 🔍 问题分析
HTTP 522错误表示：
- DNS解析正常 ✅
- Cloudflare可以找到域名 ✅ 
- 但无法连接到原始服务器 ❌

## 🛠️ 解决方案

### 方案1：检查Cloudflare Pages设置

1. **访问Cloudflare Pages**：
   - 进入：https://dash.cloudflare.com
   - Pages → beee-media 项目
   - 转到"自定义域"选项卡

2. **确认域名配置**：
   - 确保 `beeemedia.com` 显示为"有效"
   - 检查是否添加了 `www.beeemedia.com`
   - 如果没有，点击"添加自定义域"

3. **添加www域名**：
   ```
   域名: www.beeemedia.com
   ```
   - 点击"添加域名"
   - 等待验证完成

### 方案2：检查DNS配置

1. **访问DNS管理**：
   - Cloudflare控制台 → beeemedia.com → DNS

2. **确认DNS记录**：
   应该有这两条记录：
   ```
   类型: CNAME | 名称: @   | 目标: beee-media.pages.dev | 代理: 已启用
   类型: CNAME | 名称: www | 目标: beee-media.pages.dev | 代理: 已启用
   ```

3. **如果www记录不存在**，添加：
   ```
   类型: CNAME
   名称: www  
   目标: beee-media.pages.dev
   代理: 已启用 (橙色云朵)
   ```

### 方案3：强制刷新SSL证书

1. **在Cloudflare Pages中**：
   - 删除 `www.beeemedia.com` 域名
   - 等待2分钟
   - 重新添加 `www.beeemedia.com`

2. **或者在DNS中**：
   - 暂时禁用www记录的代理
   - 等待1分钟
   - 重新启用代理

## ⏰ 预期修复时间

- **配置更改**: 立即
- **SSL证书生成**: 5-15分钟
- **全球生效**: 最多30分钟

## 🧪 验证步骤

修复后，测试：
```bash
# 检查DNS
nslookup www.beeemedia.com

# 检查HTTP状态
curl -I https://www.beeemedia.com

# 应该返回HTTP 200，而不是522
```

## 💡 最快解决方案

**推荐操作顺序**：
1. 确认Pages项目中添加了www.beeemedia.com域名
2. 确认DNS中有www的CNAME记录
3. 等待5-10分钟让SSL证书生成
4. 测试访问

---

**如果以上步骤完成后仍有问题，可能需要等待SSL证书自动生成完成（最多15分钟）。**
