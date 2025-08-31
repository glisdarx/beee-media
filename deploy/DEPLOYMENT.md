# TikHub 部署指南

## 🚀 部署选项

### 选项1: Cloudflare Pages (推荐 - 免费静态托管)

Cloudflare Pages 提供免费的静态网站托管服务，适合前端展示。

#### 部署步骤:

1. **准备文件**
   - 确保以下文件在项目根目录：
     - `index.html`
     - `styles.css`
     - `script.js`

2. **登录Cloudflare**
   - 访问 [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - 使用你的账户登录

3. **创建Pages项目**
   - 点击左侧菜单的 "Pages"
   - 点击 "Create a project"
   - 选择 "Connect to Git" 或 "Upload assets"

4. **连接Git仓库 (推荐)**
   - 选择你的Git仓库
   - 设置构建配置：
     - Build command: 留空 (静态文件)
     - Build output directory: `.` (根目录)
   - 点击 "Save and Deploy"

5. **上传文件 (如果选择Upload assets)**
   - 将项目文件打包为ZIP
   - 上传到Cloudflare Pages
   - 点击 "Deploy site"

6. **配置域名**
   - 部署完成后，点击 "Custom domains"
   - 添加你购买的域名
   - 按照提示配置DNS记录

### 选项2: Heroku (完整后端API)

Heroku 提供完整的应用托管服务，包含后端API功能。

#### 部署步骤:

1. **安装Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # 下载安装包: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **登录Heroku**
   ```bash
   heroku login
   ```

3. **创建Heroku应用**
   ```bash
   heroku create your-app-name
   ```

4. **设置环境变量**
   ```bash
   heroku config:set TIKHUB_API_KEY="your_api_key_here"
   ```

5. **部署应用**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **配置域名**
   ```bash
   heroku domains:add yourdomain.com
   ```

### 选项3: Vercel (现代部署平台)

Vercel 提供现代化的部署体验，支持自动部署。

#### 部署步骤:

1. **访问Vercel**
   - 访问 [vercel.com](https://vercel.com)
   - 使用GitHub账户登录

2. **导入项目**
   - 点击 "New Project"
   - 选择你的Git仓库
   - 配置构建设置

3. **部署**
   - 点击 "Deploy"
   - 等待部署完成

## 🔧 本地开发

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动开发服务器
```bash
python app.py
```

访问 http://localhost:5000

## 📁 项目结构

```
tikhubb/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # 前端逻辑
├── app.py              # Flask后端API
├── config.py           # 配置文件
├── requirements.txt    # Python依赖
├── Procfile           # Heroku配置
├── runtime.txt        # Python版本
└── DEPLOYMENT.md      # 部署说明
```

## 🌐 域名配置

### Cloudflare DNS设置

1. **添加A记录**
   - 类型: A
   - 名称: @ (或留空)
   - IPv4地址: 你的服务器IP

2. **添加CNAME记录**
   - 类型: CNAME
   - 名称: www
   - 目标: yourdomain.com

3. **SSL设置**
   - 加密模式: Full (strict)
   - 启用HTTPS重定向

### 环境变量配置

```bash
# 生产环境
export TIKHUB_API_KEY="your_api_key_here"
export FLASK_ENV="production"
export FLASK_DEBUG="false"
```

## 🔒 安全配置

### 1. API密钥保护
- 不要在代码中硬编码API密钥
- 使用环境变量存储敏感信息
- 定期轮换API密钥

### 2. CORS配置
- 限制允许的域名
- 只允许必要的HTTP方法
- 设置适当的请求头

### 3. 速率限制
- 实现API调用频率限制
- 防止恶意请求
- 监控异常访问

## 📊 性能优化

### 1. 前端优化
- 压缩CSS和JavaScript文件
- 使用CDN加载外部资源
- 启用浏览器缓存

### 2. 后端优化
- 实现数据缓存
- 优化数据库查询
- 使用异步处理

### 3. CDN配置
- 启用Cloudflare CDN
- 配置缓存策略
- 优化图片和静态资源

## 🚨 故障排除

### 常见问题

1. **部署失败**
   - 检查依赖版本兼容性
   - 验证配置文件格式
   - 查看部署日志

2. **API调用失败**
   - 检查网络连接
   - 验证API密钥
   - 查看服务器日志

3. **域名无法访问**
   - 检查DNS配置
   - 验证SSL证书
   - 确认服务器状态

### 日志查看

```bash
# Heroku
heroku logs --tail

# 本地
tail -f app.log
```

## 📞 技术支持

如果遇到部署问题，请：

1. 查看部署日志
2. 检查配置文件
3. 验证网络连接
4. 联系技术支持

## 🎯 下一步

部署完成后，你可以：

1. 配置自定义域名
2. 设置SSL证书
3. 配置CDN加速
4. 实现监控告警
5. 优化性能指标

祝你部署顺利！ 🚀
