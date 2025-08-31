# 🗄️ Supabase 数据库设置指南

## ✅ 连接状态

**Supabase连接测试成功！** 🎉

- **项目URL**: https://pkwdhbhvjmxmnkwovjxfg.supabase.co
- **API密钥**: 已配置 ✅
- **数据库架构**: 8个表定义已准备 ✅

## 📋 下一步操作

### 1. 在Supabase控制台中创建数据表

1. **访问Supabase控制台**
   - 打开: https://supabase.com/dashboard
   - 登录您的账户
   - 选择项目: `pkwdhbhvjmxmnkwovjxfg`

2. **进入SQL编辑器**
   - 点击左侧菜单的 **"SQL Editor"**
   - 点击 **"New query"**

3. **执行数据库架构**
   - 复制 `database/schema.sql` 的内容
   - 粘贴到SQL编辑器中
   - 点击 **"Run"** 执行

### 2. 验证数据表创建

执行以下SQL查询验证表是否创建成功：

```sql
-- 查看所有表
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- 应该看到以下表:
-- - users
-- - search_history  
-- - favorite_creators
-- - user_sessions
-- - api_usage_logs
-- - email_templates
-- - email_logs
-- - system_config
```

### 3. 设置行级安全策略(RLS)

架构文件已包含RLS策略，但需要确保启用：

```sql
-- 检查RLS是否启用
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

## 🔧 测试数据库功能

### 创建测试用户

```sql
-- 插入测试用户
INSERT INTO users (email, name, subscription_tier, email_verified)
VALUES ('test@beeemedia.com', 'Test User', 'free', true)
RETURNING id, email, name;
```

### 测试搜索历史

```sql
-- 插入测试搜索记录
INSERT INTO search_history (user_id, search_query, search_type, results_count)
VALUES (
    (SELECT id FROM users WHERE email = 'test@beeemedia.com'),
    'food',
    'creators',
    10
);
```

## 🚀 启动应用

### 1. 安装完整依赖

```bash
pip3 install -r requirements.txt
```

### 2. 启动后端服务

```bash
cd backend
python3 app.py
```

### 3. 测试API端点

```bash
# 健康检查
curl http://localhost:8080/api/health

# 配置检查
curl http://localhost:8080/api/config
```

## 📊 数据库表结构

### 主要表说明

| 表名 | 用途 | 关键字段 |
|------|------|----------|
| `users` | 用户信息 | id, email, name, subscription_tier |
| `search_history` | 搜索历史 | user_id, search_query, created_at |
| `favorite_creators` | 收藏创作者 | user_id, creator_unique_id |
| `user_sessions` | 用户会话 | user_id, token_hash, expires_at |
| `api_usage_logs` | API使用统计 | user_id, endpoint, response_time_ms |
| `email_logs` | 邮件发送记录 | user_id, recipient_email, status |
| `email_templates` | 邮件模板 | template_name, html_content |
| `system_config` | 系统配置 | config_key, config_value |

### 索引优化

架构已包含以下索引：
- 用户邮箱唯一索引
- 搜索历史时间索引
- 收藏创作者复合索引
- API使用统计索引

## 🔐 安全配置

### 行级安全策略(RLS)

已配置的RLS策略：
- 用户只能访问自己的数据
- 搜索历史按用户隔离
- 收藏列表按用户隔离
- 会话管理按用户隔离

### 数据验证

- 邮箱格式验证
- 密码强度要求
- API使用限制
- 会话超时管理

## 📈 监控和维护

### 数据库监控

```sql
-- 查看表大小
SELECT 
    table_name,
    pg_size_pretty(pg_total_relation_size(table_name)) as size
FROM information_schema.tables 
WHERE table_schema = 'public';

-- 查看用户数量
SELECT COUNT(*) as user_count FROM users;

-- 查看搜索历史统计
SELECT 
    DATE(created_at) as date,
    COUNT(*) as searches
FROM search_history 
GROUP BY DATE(created_at)
ORDER BY date DESC
LIMIT 10;
```

### 性能优化

- 定期清理过期会话
- 归档旧搜索历史
- 监控API使用情况
- 优化查询性能

## 🆘 故障排除

### 常见问题

1. **连接失败**
   - 检查API密钥是否正确
   - 确认项目URL正确
   - 验证网络连接

2. **权限错误**
   - 确认RLS策略正确
   - 检查用户认证状态
   - 验证API密钥权限

3. **表不存在**
   - 重新执行schema.sql
   - 检查SQL执行日志
   - 确认表名拼写正确

### 联系支持

如果遇到问题，请检查：
- Supabase项目状态
- API密钥有效性
- 网络连接状态
- 错误日志信息

---

**🎉 数据库配置完成！现在可以启动应用并测试功能了。**
