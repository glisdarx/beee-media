# 🏗️ Beee Media 项目重构计划

## 📁 新的项目结构

```
beee-media/
├── 📂 frontend/                 # 前端文件
│   ├── 📂 assets/              # 静态资源
│   │   ├── css/                # 样式文件
│   │   ├── js/                 # JavaScript文件
│   │   ├── images/             # 图片资源
│   │   └── icons/              # 图标和favicon
│   ├── 📂 components/          # 可复用组件
│   ├── 📂 pages/               # 页面文件
│   └── 📂 templates/           # HTML模板
├── 📂 backend/                 # 后端服务
│   ├── 📂 api/                 # API路由
│   │   ├── auth.py             # 认证相关
│   │   ├── creators.py         # 创作者搜索
│   │   ├── users.py            # 用户管理
│   │   └── trends.py           # 趋势数据
│   ├── 📂 services/            # 业务逻辑
│   │   ├── supabase_client.py  # 数据库服务
│   │   ├── tikhub_client.py    # TikHub API
│   │   ├── sendgrid_client.py  # 邮箱服务
│   │   └── auth_service.py     # 认证服务
│   ├── 📂 models/              # 数据模型
│   │   ├── user.py             # 用户模型
│   │   ├── creator.py          # 创作者模型
│   │   └── search_history.py   # 搜索历史
│   ├── 📂 utils/               # 工具函数
│   ├── 📂 config/              # 配置文件
│   └── app.py                  # 主应用文件
├── 📂 database/                # 数据库相关
│   ├── 📂 migrations/          # 数据库迁移
│   ├── 📂 seeds/               # 初始数据
│   └── schema.sql              # 数据库架构
├── 📂 deployment/              # 部署配置
│   ├── cloudflare/             # Cloudflare配置
│   ├── docker/                 # Docker配置
│   └── scripts/                # 部署脚本
├── 📂 docs/                    # 项目文档
├── 📂 tests/                   # 测试文件
└── 📂 tools/                   # 开发工具
```

## 🚀 技术栈升级

### 前端
- **框架**: 保持现有的HTML/CSS/JS，后续可考虑Vue.js
- **样式**: 继续使用现有的Beee Media设计系统
- **认证**: 集成Google OAuth + 邮箱登录

### 后端
- **框架**: Flask → 逐步升级到Flask-RESTful
- **数据库**: Supabase (PostgreSQL)
- **认证**: Google OAuth 2.0 + JWT
- **邮箱**: SendGrid API
- **API**: TikHub集成优化

### 基础设施
- **部署**: Cloudflare Pages (前端) + Cloudflare Workers (后端)
- **数据库**: Supabase
- **CDN**: Cloudflare
- **监控**: 后续添加

## 📊 数据库设计

### 用户表 (users)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);
```

### 搜索历史表 (search_history)
```sql
CREATE TABLE search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    search_query VARCHAR(255) NOT NULL,
    filters JSONB,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 收藏的创作者 (favorite_creators)
```sql
CREATE TABLE favorite_creators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    creator_unique_id VARCHAR(255) NOT NULL,
    creator_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, creator_unique_id)
);
```

## 🔐 认证流程

### Google OAuth
1. 用户点击"Google登录"
2. 重定向到Google OAuth
3. 获取用户信息并创建/更新用户记录
4. 生成JWT token
5. 前端存储token并管理认证状态

### 邮箱注册
1. 用户输入邮箱
2. 发送验证邮件 (SendGrid)
3. 用户点击验证链接
4. 创建账户并自动登录

## 📧 邮箱服务功能

### SendGrid集成
- **欢迎邮件**: 新用户注册
- **邮箱验证**: 验证邮箱地址
- **密码重置**: 重置密码链接
- **搜索报告**: 定期发送搜索结果
- **通知邮件**: 重要功能更新

## 🛡️ 安全考虑

- **JWT Token**: 用户认证
- **环境变量**: 敏感信息保护
- **CORS**: 跨域请求控制
- **Rate Limiting**: API调用限制
- **数据验证**: 输入数据验证

## 📈 功能规划

### Phase 1: 基础重构 (当前)
- ✅ 项目结构重组
- ✅ Supabase数据库设置
- ✅ 用户认证系统
- ✅ SendGrid邮箱集成

### Phase 2: 功能完善
- 🔄 TikHub API修复
- 🔄 用户仪表板
- 🔄 搜索历史管理
- 🔄 创作者收藏功能

### Phase 3: 高级功能
- 🔄 付费订阅系统
- 🔄 高级搜索功能
- 🔄 数据导出功能
- 🔄 团队协作功能

## 🎯 立即行动项

1. **重组文件结构**
2. **设置Supabase数据库**
3. **实现基础认证系统**
4. **集成SendGrid邮箱服务**
5. **创建用户注册/登录页面**
