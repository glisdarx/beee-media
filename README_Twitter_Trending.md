# Twitter趋势数据获取工具

## 📋 功能概述

这个工具可以获取全球多个国家的Twitter趋势数据，并将结果保存为CSV格式。

## 🚀 快速开始

### 1. 运行脚本

```bash
python3 multi_country_trending.py
```

### 2. 选择国家

脚本会显示支持的国家列表，你可以选择：

- **单个国家**: 输入国家名称，如 `UnitedStates`
- **多个国家**: 用逗号分隔，如 `UnitedStates,China,Japan`
- **所有国家**: 输入 `all`

### 3. 查看结果

脚本会自动将结果保存到 `output/` 文件夹中，文件名格式为：
```
twitter_trending_{国家名}_{时间戳}.csv
```

## 🌍 支持的国家

脚本支持以下58个国家：

1. UnitedStates (美国)
2. China (中国)
3. India (印度)
4. Japan (日本)
5. Russia (俄罗斯)
6. Germany (德国)
7. Indonesia (印尼)
8. Brazil (巴西)
9. France (法国)
10. UnitedKingdom (英国)
11. Turkey (土耳其)
12. Italy (意大利)
13. Mexico (墨西哥)
14. SouthKorea (韩国)
15. Canada (加拿大)
16. Spain (西班牙)
17. SaudiArabia (沙特阿拉伯)
18. Egypt (埃及)
19. Australia (澳大利亚)
20. Poland (波兰)
21. Iran (伊朗)
22. Pakistan (巴基斯坦)
23. Vietnam (越南)
24. Nigeria (尼日利亚)
25. Bangladesh (孟加拉国)
26. Netherlands (荷兰)
27. Argentina (阿根廷)
28. Philippines (菲律宾)
29. Malaysia (马来西亚)
30. Colombia (哥伦比亚)
31. UniteArabEmirates (阿联酋)
32. Romania (罗马尼亚)
33. Belgium (比利时)
34. Switzerland (瑞士)
35. Singapore (新加坡)
36. Sweden (瑞典)
37. Norway (挪威)
38. Austria (奥地利)
39. Kazakhstan (哈萨克斯坦)
40. Algeria (阿尔及利亚)
41. Chile (智利)
42. Czechia (捷克)
43. Peru (秘鲁)
44. Iraq (伊拉克)
45. Israel (以色列)
46. Ukraine (乌克兰)
47. Denmark (丹麦)
48. Portugal (葡萄牙)
49. Hungary (匈牙利)
50. Greece (希腊)
51. Finland (芬兰)
52. NewZealand (新西兰)
53. Belarus (白俄罗斯)
54. Slovakia (斯洛伐克)
55. Serbia (塞尔维亚)
56. Lithuania (立陶宛)
57. Luxembourg (卢森堡)
58. Estonia (爱沙尼亚)

## 📊 数据字段

生成的CSV文件包含以下字段：

- **name**: 趋势话题名称
- **context**: 趋势分类和上下文
- **description**: 趋势描述（如推文数量）

## 📈 数据示例

### 美国趋势示例
```
name,context,description
HAMNET,,Promoted by Focus Features
Trans,Politics · Trending,966K posts
Minneapolis,Politics · Trending,
Minnesota,Politics · Trending,442K posts
Taylor,Trending,
```

### 中国趋势示例
```
name,context,description
HAMNET,,Promoted by Focus Features
Cambodian,Trending,"4,125 posts"
#WhaleStorexoxoFinalEP,Only on X · Trending,8.27M posts
#和合之路,Trending,
```

### 日本趋势示例
```
name,context,description
HAMNET,,Promoted by Focus Features
松竹座閉館,J-pop · Trending,14.6K posts
JUMP,J-pop · Trending,155K posts
#ポケポケ,Trending,"6,656 posts"
```

## 🔧 技术细节

### API端点
- **URL**: `https://api.tikhub.io/api/v1/twitter/web/fetch_trending`
- **方法**: GET
- **认证**: Bearer Token

### 参数
- **country**: 国家代码（必需）

### 响应格式
```json
{
  "code": 200,
  "request_id": "xxx",
  "router": "/api/v1/twitter/web/fetch_trending",
  "data": {
    "trends": [
      {
        "name": "趋势名称",
        "description": "描述",
        "context": "分类"
      }
    ]
  }
}
```

## 📝 使用场景

1. **市场研究**: 了解不同国家的热门话题
2. **内容营销**: 发现热门话题进行内容创作
3. **品牌监控**: 监控品牌相关话题
4. **趋势分析**: 分析不同地区的兴趣差异
5. **新闻监测**: 实时了解全球热点事件

## ⚠️ 注意事项

1. **API限制**: 请遵守TikHub的API使用限制
2. **请求频率**: 脚本已内置1秒延迟，避免请求过快
3. **数据时效性**: 趋势数据会实时更新，建议定期获取
4. **文件管理**: 生成的CSV文件会按时间戳命名，避免覆盖

## 🛠️ 依赖要求

- Python 3.6+
- requests
- 有效的TikHub API密钥

确保 `config.py` 文件中包含正确的API密钥：
```python
TIKHUB_API_KEY = "your_api_key_here"
``` 