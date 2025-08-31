# 🚀 Cloudflare API 一键部署指南

## 📋 您的部署信息

- **API Token**: `cd226a2bc1a1ff06d8408b7ef12df5b4`
- **域名**: `beeemedia.com`
- **GitHub仓库**: `https://github.com/glisdarx/beee-media`
- **项目名称**: `beee-media`

## 🔧 API令牌问题排查

当前API令牌格式似乎不正确。Cloudflare API令牌通常：
- 长度为40个字符
- 以字母开头
- 包含字母数字字符

请检查您的API令牌是否为：
1. **Global API Key** (不推荐)
2. **API Token** (推荐)

## 🌟 方案一：快速Web部署 (推荐)

由于API令牌格式问题，建议您使用Web界面快速部署：

### 步骤：

1. **访问 Cloudflare Dashboard**
   ```
   https://dash.cloudflare.com
   ```

2. **创建Pages项目**
   - 点击左侧菜单 "Pages"
   - 点击 "Create a project"
   - 选择 "Connect to Git"

3. **连接GitHub**
   - 授权Cloudflare访问GitHub
   - 选择仓库：`glisdarx/beee-media`

4. **配置构建设置**
   ```
   Project name: beee-media
   Production branch: main
   Framework preset: None
   Build command: echo "Static deployment ready"
   Build output directory: /
   ```

5. **设置环境变量**
   ```
   Variable name: TIKHUB_API_KEY
   Value: w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA==
   ```

6. **部署**
   - 点击 "Save and Deploy"
   - 等待2-3分钟部署完成

7. **配置自定义域名**
   - 在项目页面点击 "Custom domains"
   - 添加：`beeemedia.com`
   - Cloudflare会自动配置DNS

## 🔄 方案二：修复API令牌

如果您想使用API自动部署，请：

1. **获取正确的API令牌**
   - 访问：https://dash.cloudflare.com/profile/api-tokens
   - 点击 "Create Token"
   - 选择 "Pages:Edit" 模板
   - 配置权限：
     - Zone Resources: Include All zones
     - Account Resources: Include All accounts

2. **使用新令牌**
   ```bash
   # 替换为新的API令牌
   export CLOUDFLARE_API_TOKEN="your-new-token-here"
   python3 cloudflare-api-deploy.py
   ```

## 🎯 部署完成后验证

访问以下URL确认部署成功：

- ✅ **主页**: https://beeemedia.com
- ✅ **创作者搜索**: https://beeemedia.com/creators
- ✅ **API功能**: 在创作者页面测试搜索

## 📞 故障排除

### 常见问题：

1. **API令牌无效**
   - 检查令牌权限
   - 确认令牌未过期
   - 使用正确的令牌格式

2. **域名解析问题**
   - 等待DNS生效（5-10分钟）
   - 检查Cloudflare DNS设置

3. **构建失败**
   - 检查GitHub仓库权限
   - 确认分支名称为 `main`

## 🚀 推荐做法

**立即行动方案**：
1. 使用Web界面部署（5分钟完成）
2. 后续可以优化API自动化流程

---

📝 **注意**: 所有代码已经推送到GitHub，配置文件都已准备就绪，只需要在Cloudflare中创建Pages项目即可！
