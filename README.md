# TikHub - TikTok数据趋势分析平台

![TikHub Logo](https://img.shields.io/badge/TikHub-TikTok%20Data%20Analytics-blue?style=for-the-badge&logo=tiktok)

一个现代化的TikTok数据分析和趋势监测平台，支持全球58个国家的实时趋势数据获取和分析。

## ✨ 主要功能

### 🌍 全球趋势分析
- 支持58个国家的实时趋势数据
- 智能国家选择器，支持多选和全选
- 实时数据更新和趋势监测
- 多维度数据分类和统计

### 📊 数据可视化
- 交互式图表展示
- 热门话题分布图
- 分类统计饼图
- 实时数据统计卡片

### 👥 创作者数据分析
- 关键词搜索创作者
- 粉丝、关注、获赞等数据统计
- 创作者认证状态显示
- 地理位置信息展示

### 💾 数据导出
- 支持CSV格式导出
- 支持JSON格式导出
- 自定义数据筛选
- 批量数据处理

## 🚀 快速开始

### 本地开发

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/tikhubb.git
   cd tikhubb
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**
   ```bash
   # 编辑 config.py 文件
   TIKHUB_API_KEY = "your_api_key_here"
   ```

4. **启动开发服务器**
   ```bash
   python app.py
   ```

5. **访问应用**
   打开浏览器访问 http://localhost:5000

### 生产部署

#### 选项1: Cloudflare Pages (推荐)
- 免费静态托管
- 全球CDN加速
- 自动SSL证书
- 详细部署步骤请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

#### 选项2: Heroku
- 完整后端API支持
- 自动部署
- 详细部署步骤请查看 [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🛠️ 技术栈

### 前端
- **HTML5** - 语义化标记
- **CSS3** - 现代化样式和动画
- **JavaScript ES6+** - 交互逻辑
- **Chart.js** - 数据可视化
- **Font Awesome** - 图标库

### 后端
- **Python 3.11+** - 主要编程语言
- **Flask** - Web框架
- **Flask-CORS** - 跨域支持
- **Requests** - HTTP客户端
- **Pandas** - 数据处理

### 部署
- **Cloudflare Pages** - 静态托管
- **Heroku** - 应用托管
- **Gunicorn** - WSGI服务器

## 📁 项目结构

```
tikhubb/
├── index.html              # 主页面
├── styles.css              # 样式文件
├── script.js               # 前端逻辑
├── app.py                  # Flask后端API
├── config.py               # 配置文件
├── requirements.txt        # Python依赖
├── Procfile               # Heroku配置
├── runtime.txt            # Python版本
├── DEPLOYMENT.md          # 部署说明
├── README.md              # 项目说明
└── output/                # 数据输出目录
    ├── *.csv              # CSV数据文件
    └── *.json             # JSON数据文件
```

## 🌐 API接口

### 趋势数据接口
```http
POST /api/trends
Content-Type: application/json

{
  "countries": ["UnitedStates", "China", "Japan"]
}
```

### 创作者搜索接口
```http
POST /api/creators
Content-Type: application/json

{
  "keyword": "AI",
  "max_creators": 20,
  "include_videos": true
}
```

### 国家列表接口
```http
GET /api/countries
```

## 🎨 界面预览

### 主要特性
- 🎯 响应式设计，支持所有设备
- 🌈 现代化UI设计，美观易用
- 📱 移动端优化，触控友好
- ⚡ 快速加载，流畅体验
- 🔍 智能搜索，精准结果

### 界面截图
- 英雄区域：展示平台核心价值
- 趋势分析：国家选择和数据展示
- 创作者数据：搜索和结果展示
- 关于我们：功能介绍和特色说明

## 🔒 安全特性

- API密钥环境变量管理
- CORS跨域安全配置
- 请求频率限制
- 输入数据验证
- 错误信息过滤

## 📊 性能优化

- 静态资源CDN加速
- 图片懒加载
- 代码分割和压缩
- 浏览器缓存优化
- 异步数据加载

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📝 文档改进
- 🎨 UI/UX优化
- 🧪 测试用例

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [TikHub API](https://tikhub.io/) - 提供TikTok数据接口
- [Chart.js](https://www.chartjs.org/) - 数据可视化库
- [Font Awesome](https://fontawesome.com/) - 图标库
- [Flask](https://flask.palletsprojects.com/) - Python Web框架

## 📞 联系我们

- 🌐 网站: [https://tikhubb.com](https://tikhubb.com)
- 📧 邮箱: info@tikhubb.com
- 💬 问题反馈: [GitHub Issues](https://github.com/yourusername/tikhubb/issues)

## 🚀 部署状态

[![Deploy to Cloudflare Pages](https://img.shields.io/badge/Deploy%20to-Cloudflare%20Pages-blue?style=for-the-badge&logo=cloudflare)](https://dash.cloudflare.com/pages)
[![Deploy to Heroku](https://img.shields.io/badge/Deploy%20to-Heroku-purple?style=for-the-badge&logo=heroku)](https://heroku.com/deploy)

---

⭐ 如果这个项目对你有帮助，请给我们一个星标！
