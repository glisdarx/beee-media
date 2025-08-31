# TikHub API 字段映射表

## API 响应结构
```
{
  "data": {
    "status_code": 0,           // 成功状态码
    "result_status": 4,         // 结果状态
    "has_more": true,           // 是否有更多数据
    "data": [                   // 视频列表
      {
        "type": 1,              // 类型：1=视频
        "aweme_info": {         // 视频信息
          "author": {           // 作者信息
            "nickname": "Briangelecooks",
            "unique_id": "briangelecooks",
            "follower_count": 288962,
            "aweme_count": 0,
            "total_favorited": 0,
            "signature": "个人简介",
            "sec_uid": "MS4wLjABAAAAsOZ8Av3W6hd4ByDoQ4UMsK_9SrKRnJVoriKxw4FY_QiMhHHb23hTKggBL7u__ljP"
          },
          "statistics": {       // 视频统计
            "play_count": 6196667,
            "digg_count": 984646,
            "comment_count": 4606,
            "share_count": 82071
          },
          "aweme_id": "7544492470596373773",
          "create_time": 1756623948572
        }
      }
    ]
  }
}
```

## 前端展示字段映射

| 前端字段 | API字段路径 | 说明 |
|---------|------------|------|
| search_keyword | 用户输入 | 搜索关键词 |
| nickname | aweme_info.author.nickname | 创作者昵称 |
| unique_id | aweme_info.author.unique_id | 唯一ID |
| follower_count | aweme_info.author.follower_count | 粉丝数 |
| total_video_count | aweme_info.author.aweme_count | 视频总数 |
| total_likes_count | aweme_info.author.total_favorited | 总点赞数 |
| tiktok_account_url | 构建 | https://tiktok.com/@{unique_id} |
| tiktok_account_bio_description | aweme_info.author.signature | 个人简介 |
| bio_link_url | 从signature中提取 | 个人链接 |
| language | 从signature中检测 | 语言设置 |
| latest_video_link | 构建 | https://tiktok.com/@{unique_id}/video/{aweme_id} |
| latest_video_play_count | aweme_info.statistics.play_count | 最新视频播放量 |
| second_latest_video_link | 需要额外API调用 | 第二新视频链接 |
| second_latest_video_play_count | 需要额外API调用 | 第二新视频播放量 |
| third_latest_video_link | 需要额外API调用 | 第三新视频链接 |
| third_latest_video_play_count | 需要额外API调用 | 第三新视频播放量 |
| fourth_latest_video_link | 需要额外API调用 | 第四新视频链接 |
| fourth_latest_video_play_count | 需要额外API调用 | 第四新视频播放量 |
| fifth_latest_video_link | 需要额外API调用 | 第五新视频链接 |
| fifth_video_play_count | 需要额外API调用 | 第五视频播放量 |
| days_since_last_video | 计算 | 基于create_time计算 |
| avg_video_play_count | 计算 | 基于play_count计算 |
| median_view_count | 计算 | 基于play_count计算 |
| expected_price | 计算 | 基于follower_count和total_favorited计算 |
| email | 从signature中提取 | 邮箱地址 |

## 问题分析

1. **API响应结构问题**：
   - 顶层没有status_code，而是在data.status_code
   - 需要检查data.status_code而不是result.status_code

2. **字段路径问题**：
   - 作者信息在aweme_info.author
   - 统计信息在aweme_info.statistics
   - 视频ID在aweme_info.aweme_id

3. **数据获取限制**：
   - 当前API只返回单个视频的作者信息
   - 需要额外API调用来获取作者的其他视频信息
