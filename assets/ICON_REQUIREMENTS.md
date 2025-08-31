# Beee Media 图标文件需求清单

## 需要的图标文件

当您提供 Beee Media 的 logo 图片后，我们需要生成以下尺寸的图标文件：

### Favicon 系列
- `favicon.ico` - 传统favicon文件（16x16, 32x32, 48x48）
- `favicon-16x16.png` - 16x16 PNG格式
- `favicon-32x32.png` - 32x32 PNG格式

### Apple Touch 图标
- `apple-touch-icon.png` - 180x180 PNG格式（iOS设备使用）

### Android 图标
- `android-chrome-192x192.png` - 192x192 PNG格式
- `android-chrome-512x512.png` - 512x512 PNG格式

### Windows 图标
- `mstile-150x150.png` - 150x150 PNG格式（Windows磁贴）

### 社交媒体图片
- `og-image.jpg` - 1200x630 JPEG格式（Facebook Open Graph）
- `twitter-image.jpg` - 1200x600 JPEG格式（Twitter卡片）
- `creators-og-image.jpg` - 1200x630 JPEG格式（创作者页面专用）
- `creators-twitter-image.jpg` - 1200x600 JPEG格式（创作者页面Twitter卡片）

### 品牌Logo
- `logo.png` - 高分辨率品牌logo（推荐512x512或更大）

## 设计要求

### 颜色规范
- 主色调：**蜜黄色 (#FFD93D)**
- 辅助色：深灰色或深蓝色
- 背景色：白色 (#FFFFFF)

### 设计风格
- 简约现代
- 蜜蜂/蜂蜜元素
- 符合 "Beee Media" 品牌形象
- 在小尺寸下仍然清晰可辨

### 技术要求
- PNG文件使用透明背景（除非特别说明）
- ICO文件包含多个尺寸
- JPEG文件用于社交媒体分享
- 所有图片经过优化压缩

## 如何使用

1. 将您的 logo 图片放入此目录
2. 使用在线工具或设计软件生成所需尺寸
3. 推荐工具：
   - https://realfavicongenerator.net/ （自动生成所有尺寸）
   - https://favicon.io/ （favicon生成器）
   - Photoshop/Figma/Sketch （手动调整）

## 文件命名规范

请严格按照上述文件名命名，因为HTML中的引用路径已经配置好。

所有文件都应该放在 `/assets/` 目录下。
