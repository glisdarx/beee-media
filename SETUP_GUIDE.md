# 🚀 Beee Media 项目设置指南

## 📋 当前进度

✅ **已完成**:
- 项目结构重组
- Supabase数据库架构设计
- 用户认证系统（Google OAuth + 邮箱）
- SendGrid邮箱服务集成
- API路由和服务架构

🔄 **待完成**:
- 前端登录注册页面
- 主应用文件更新
- TikHub API修复
- 环境变量配置

## 🗂️ 新的项目结构

```
📁 beee-media/
├── 📂 backend/           # 后端服务
│   ├── api/             # API路由
│   ├── services/        # 业务逻辑
│   ├── models/          # 数据模型
│   ├── utils/           # 工具函数
│   └── config/          # 配置文件
├── 📂 frontend/         # 前端文件
│   ├── pages/           # HTML页面
│   ├── assets/          # 静态资源
│   └── components/      # 组件
├── 📂 database/         # 数据库相关
└── 📂 deployment/       # 部署配置
```

## 🗄️ 数据库设置

### 1. 创建Supabase项目
1. 访问 https://supabase.com
2. 创建新项目
3. 获取 URL 和 API 密钥

### 2. 执行数据库架构
```sql
-- 在Supabase SQL编辑器中执行 database/schema.sql
```

### 3. 主要数据表
- `users` - 用户信息
- `search_history` - 搜索历史
- `favorite_creators` - 收藏的创作者
- `user_sessions` - 用户会话
- `api_usage_logs` - API使用日志
- `email_logs` - 邮件发送记录

## 📧 SendGrid邮箱配置

### 1. 获取API密钥
1. 注册 https://sendgrid.com
2. 创建API密钥
3. 验证发送域名

### 2. 邮件模板
- 欢迎邮件
- 邮箱验证
- 密码重置
- 搜索报告

## 🔐 认证系统功能

### 支持的登录方式
1. **Google OAuth** - 一键登录
2. **邮箱注册** - 传统注册流程

### 安全特性
- JWT token认证
- 密码加密（bcrypt）
- 邮箱验证
- 密码重置
- 会话管理
- API使用限制

## 🌐 API端点

### 认证相关 (`/api/auth/`)
- `POST /register` - 邮箱注册
- `POST /login` - 邮箱登录
- `POST /google-login` - Google登录
- `POST /verify-email` - 邮箱验证
- `POST /forgot-password` - 忘记密码
- `POST /reset-password` - 重置密码
- `GET /profile` - 获取用户资料
- `PUT /profile` - 更新用户资料
- `GET /check-usage` - 检查API使用情况

### 创作者搜索 (`/api/creators/`)
- `POST /search` - 搜索创作者
- `GET /favorites` - 获取收藏
- `POST /favorites` - 添加收藏
- `DELETE /favorites/:id` - 移除收藏

## ⚙️ 环境变量设置

复制 `env.example` 为 `.env` 并配置:

```bash
# 必需配置
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key
SENDGRID_API_KEY=your-sendgrid-key
JWT_SECRET_KEY=your-jwt-secret

# 可选配置
GOOGLE_CLIENT_ID=your-google-client-id
FLASK_ENV=development
```

## 🚀 本地开发启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp env.example .env
# 编辑 .env 文件填入实际值
```

### 3. 启动开发服务器
```bash
cd backend
python app.py
```

## 📱 下一步计划

### 立即任务
1. **创建前端登录页面** - 用户注册/登录界面
2. **更新主应用** - 集成新的认证系统
3. **修复TikHub API** - 确保搜索功能正常

### 后续功能
1. **用户仪表板** - 显示使用统计
2. **搜索历史** - 查看和管理历史记录
3. **收藏管理** - 创作者收藏功能
4. **付费订阅** - 高级功能解锁

## 🔧 开发工具

### 推荐的开发环境
- **后端**: Python 3.9+, Flask
- **前端**: 现有的HTML/CSS/JS
- **数据库**: Supabase (PostgreSQL)
- **部署**: Cloudflare Pages + Workers

### 调试技巧
- 使用 `FLASK_DEBUG=true` 启用调试模式
- 检查 `logs/app.log` 获取详细日志
- 在Supabase控制台中监控数据库操作

## 📞 支持

如果遇到问题：
1. 检查环境变量配置
2. 查看服务器日志
3. 验证数据库连接
4. 确认API密钥有效性

---

**项目已经具备完整的用户管理和认证系统！** 🎉

下一步是创建前端界面来使用这些功能。
