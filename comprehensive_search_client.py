#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于综合搜索API的TikTok创作者数据收集客户端
"""

import requests
import json
import logging
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from config import TIKHUB_API_KEY, TIKHUB_BASE_URL

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveSearchClient:
    """综合搜索API客户端"""
    
    def __init__(self):
        self.base_url = TIKHUB_BASE_URL
        self.api_key = TIKHUB_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "TikTok-Automation/2.0"
        }
    
    def _make_request(self, url: str, params: Dict = None, max_retries: int = 3) -> Optional[Dict]:
        """发送API请求，带重试机制"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                logger.debug(f"请求URL: {response.url}")
                logger.debug(f"响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries}): {response.status_code} - {response.text[:100]}...")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # 指数退避
                    continue
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
        
        logger.error(f"所有重试尝试失败，URL: {url}")
        return None
    
    def comprehensive_search(self, keyword: str, count: int = 20, sort_type: int = 0) -> List[Dict]:
        """
        综合搜索指定关键词
        
        Args:
            keyword: 搜索关键词
            count: 返回数量
            sort_type: 0-相关度，1-最多点赞
            
        Returns:
            List[Dict]: 搜索结果中的视频列表
        """
        url = f"{self.base_url}/api/v1/tiktok/app/v3/fetch_general_search_result"
        
        params = {
            "keyword": keyword,
            "offset": 0,
            "count": count,
            "sort_type": sort_type,
            "publish_time": 0  # 0-不限制时间
        }
        
        logger.info(f"🔍 综合搜索关键词: {keyword}")
        
        # 高并发优化：减少请求间隔
        time.sleep(0.3)  # 减少到0.3秒，支持高并发
        
        result = self._make_request(url, params)
        if not result:
            logger.warning(f"第一次请求失败，等待后重试...")
            time.sleep(2)  # 减少重试等待时间
            result = self._make_request(url, params)
            if not result:
                return []
        
        # 解析数据结构
        data = result.get("data", {})
        items = data.get("data", [])
        
        videos = []
        for item in items:
            # 只处理视频类型的内容
            if item.get("type") == 1 and "aweme_info" in item:
                aweme_info = item["aweme_info"]
                videos.append(aweme_info)
        
        logger.info(f"✅ 找到 {len(videos)} 个相关视频")
        return videos
    
    def extract_creators_from_videos(self, videos: List[Dict]) -> List[Dict]:
        """从视频列表中提取创作者信息"""
        creators = {}  # 使用字典去重
        
        for video in videos:
            author = video.get("author", {})
            if not author:
                continue
            
            user_id = author.get("uid") or author.get("sec_uid", "")
            if not user_id:
                continue
            
            # 提取基本信息
            creator_info = {
                "user_id": user_id,
                "sec_user_id": author.get("sec_uid", ""),
                "nickname": author.get("nickname", ""),
                "unique_id": author.get("unique_id", ""),
                "signature": author.get("signature", ""),
                "follower_count": author.get("follower_count", 0),
                "following_count": author.get("following_count", 0),
                "aweme_count": author.get("aweme_count", 0),  # 视频数量
                "total_favorited": author.get("total_favorited", 0),  # 总点赞数
                "avatar_url": author.get("avatar_larger", {}).get("url_list", [""])[0] if author.get("avatar_larger") else "",
                "verified": author.get("verification_type", 0) > 0,
                "tiktok_account_url": self._generate_tiktok_url(author.get("unique_id", ""))
            }
            
            # 使用unique_id作为key去重
            key = creator_info["unique_id"] or creator_info["user_id"]
            if key and key not in creators:
                creators[key] = creator_info
        
        logger.info(f"✅ 提取到 {len(creators)} 个唯一创作者")
        return list(creators.values())
    
    def get_user_profile(self, unique_id: str = None, sec_user_id: str = None) -> Optional[Dict]:
        """获取用户详细资料"""
        if not unique_id and not sec_user_id:
            return None
        
        url = f"{self.base_url}/api/v1/tiktok/app/v3/handler_user_profile"
        
        params = {}
        if unique_id:
            params["unique_id"] = unique_id
        elif sec_user_id:
            params["sec_user_id"] = sec_user_id
        
        logger.debug(f"获取用户资料: {unique_id or sec_user_id}")
        
        result = self._make_request(url, params)
        if result and result.get("code") == 200:
            return result.get("data", {})
        
        return None
    
    def get_user_profile_web(self, unique_id: str = None, sec_uid: str = None) -> Optional[Dict]:
        """获取用户详细资料（Web API版本，包含bioLink和language数据）"""
        if not unique_id and not sec_uid:
            return None
        
        url = f"{self.base_url}/api/v1/tiktok/web/fetch_user_profile"
        
        params = {}
        if unique_id:
            params["uniqueId"] = unique_id
        elif sec_uid:
            params["secUid"] = sec_uid
        
        logger.debug(f"获取用户资料(Web): {unique_id or sec_uid}")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result and result.get("code") == 200:
                data = result.get("data", "")
                if isinstance(data, str):
                    try:
                        return json.loads(data)
                    except json.JSONDecodeError:
                        logger.warning(f"无法解析用户资料JSON数据: {data[:100]}...")
                        return None
                else:
                    return data
            
            logger.warning(f"获取用户资料失败: {result.get('code')} - {result.get('message', 'No message')}")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求用户资料失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"解析用户资料JSON失败: {e}")
            return None
    
    def get_user_videos(self, sec_user_id: str, count: int = 10) -> List[Dict]:
        """获取用户的视频列表"""
        url = f"{self.base_url}/api/v1/tiktok/app/v3/fetch_user_post_videos"
        
        params = {
            "sec_user_id": sec_user_id,
            "max_cursor": 0,
            "count": count
        }
        
        logger.debug(f"获取用户视频: {sec_user_id}")
        
        result = self._make_request(url, params)
        if result and result.get("code") == 200:
            data = result.get("data", {})
            return data.get("aweme_list", [])
        
        return []
    
    def enhance_creator_data(self, creator: Dict) -> Dict:
        """增强创作者数据，获取更详细的信息和视频数据"""
        enhanced = creator.copy()
        
        # 获取用户详细资料（App API）
        profile = self.get_user_profile(
            unique_id=creator.get("unique_id"),
            sec_user_id=creator.get("sec_user_id")
        )
        
        if profile:
            user_info = profile.get("user", {})
            # 更新更准确的数据
            enhanced.update({
                "follower_count": user_info.get("follower_count", creator.get("follower_count", 0)),
                "aweme_count": user_info.get("aweme_count", creator.get("aweme_count", 0)),
                "total_favorited": user_info.get("total_favorited", creator.get("total_favorited", 0)),
                "signature": user_info.get("signature", creator.get("signature", "")),
                "verified": user_info.get("verification_type", 0) > 0
            })
        
        # 获取用户详细资料（Web API，包含bioLink和language数据）
        web_profile = self.get_user_profile_web(
            unique_id=creator.get("unique_id"),
            sec_uid=creator.get("sec_user_id")
        )
        
        if web_profile:
            user_info_web = web_profile.get("userInfo", {}).get("user", {})
            
            # 提取bioLink数据
            bio_link = user_info_web.get("bioLink", {})
            if bio_link:
                enhanced["bio_link_url"] = bio_link.get("link", "")
            else:
                enhanced["bio_link_url"] = ""
            
            # 提取language数据
            language = user_info_web.get("language", "")
            enhanced["language"] = language if language else ""
        else:
            enhanced["bio_link_url"] = ""
            enhanced["language"] = ""
        
        # 获取用户最新视频
        videos = self.get_user_videos(creator.get("sec_user_id", ""), count=15)  # 获取更多视频，然后按时间排序
        video_data = []
        latest_video_timestamp = None
        
        # 按创建时间降序排序，确保获取时间维度上的最新视频（而不是置顶视频）
        if videos:
            logger.debug(f"排序前视频数量: {len(videos)}")
            videos = sorted(videos, key=lambda x: x.get("create_time", 0), reverse=True)
            videos = videos[:5]  # 只取最新的5个
            logger.debug(f"按时间排序后取最新5个视频，create_time: {[v.get('create_time', 0) for v in videos]}")
        
        for i, video in enumerate(videos[:5]):
            # 获取视频时间戳
            create_time = video.get("create_time", 0)
            if i == 0:  # 第一个视频是最新的（按时间排序后）
                latest_video_timestamp = create_time
            
            video_info = {
                f"video_{i+1}_link": self._generate_video_url(video.get("aweme_id", "")),
                f"video_{i+1}_play_count": video.get("statistics", {}).get("play_count", 0),
                f"video_{i+1}_desc": video.get("desc", "")[:100] + "..." if len(video.get("desc", "")) > 100 else video.get("desc", ""),
                f"video_{i+1}_timestamp": create_time
            }
            video_data.append(video_info)
        
        # 计算最新视频距今天数
        days_since_last_video = self._calculate_days_since_video(latest_video_timestamp) if latest_video_timestamp else -1
        
        # 添加视频数据到enhanced对象
        for video_info in video_data:
            enhanced.update(video_info)
        
        # 添加新字段
        enhanced["days_since_last_video"] = days_since_last_video
        
        # 高并发优化：减少延迟
        time.sleep(0.15)  # 减少到0.15秒，提高处理速度
        
        return enhanced
    
    def _generate_tiktok_url(self, unique_id: str) -> str:
        """生成TikTok账户URL"""
        if not unique_id:
            return ""
        return f"https://www.tiktok.com/@{unique_id}"
    
    def _generate_video_url(self, aweme_id: str) -> str:
        """生成TikTok视频URL"""
        if not aweme_id:
            return ""
        return f"https://www.tiktok.com/@unknown/video/{aweme_id}"
    
    def _extract_email_from_bio(self, bio: str) -> str:
        """从个人简介中提取邮箱地址"""
        if not bio:
            return ""
        
        # 邮箱正则表达式
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # 查找所有邮箱
        emails = re.findall(email_pattern, bio)
        
        # 返回第一个找到的邮箱，如果有多个邮箱用分号分隔
        if emails:
            return '; '.join(emails)
        
        return ""
    
    def _calculate_days_since_video(self, video_timestamp: int) -> int:
        """计算视频发布时间距离今天的天数"""
        if not video_timestamp:
            return -1  # -1 表示无法获取时间
        
        try:
            # TikTok时间戳通常是毫秒级，转换为秒
            if video_timestamp > 1e12:  # 毫秒级时间戳
                video_timestamp = video_timestamp / 1000
            
            video_date = datetime.fromtimestamp(video_timestamp)
            today = datetime.now()
            
            # 计算天数差
            days_diff = (today - video_date).days
            return days_diff
            
        except (ValueError, OSError, OverflowError) as e:
            logger.debug(f"时间戳转换失败: {video_timestamp}, 错误: {e}")
            return -1
    
    def search_and_collect_creators(self, keyword: str, max_creators: int = 20) -> Tuple[List[Dict], List[Dict]]:
        """
        搜索关键词并收集创作者信息
        
        Returns:
            Tuple[List[Dict], List[Dict]]: (创作者基本信息, 创作者视频数据)
        """
        logger.info(f"🚀 开始收集关键词 '{keyword}' 的创作者信息")
        
        # 1. 综合搜索 - 分批搜索策略
        # API限制：单次搜索不能超过40个，所以采用分批策略
        max_single_search = 40
        total_videos = []
        
        if max_creators <= 20:
            # 小量数据：单次搜索
            search_count = min(max_creators * 2, max_single_search)
            videos = self.comprehensive_search(keyword, count=search_count)
            total_videos.extend(videos)
        else:
            # 大量数据：分批搜索
            batches = (max_creators + 19) // 20  # 向上取整
            for batch in range(min(batches, 3)):  # 最多3批，避免过多请求
                search_count = min(max_single_search, max_creators * 2 // batches)
                logger.info(f"📦 分批搜索 {batch + 1}/{min(batches, 3)}, count={search_count}")
                videos = self.comprehensive_search(keyword, count=search_count)
                total_videos.extend(videos)
                if len(total_videos) >= max_creators * 2:  # 获得足够的视频
                    break
                time.sleep(1)  # 分批间隔
        
        if not total_videos:
            logger.warning("未找到相关视频")
            return [], []
        
        logger.info(f"📊 总共获得 {len(total_videos)} 个视频")
        
        # 2. 提取创作者
        creators = self.extract_creators_from_videos(total_videos)
        if not creators:
            logger.warning("未找到创作者信息")
            return [], []
        
        logger.info(f"📊 从 {len(total_videos)} 个视频中提取到 {len(creators)} 个唯一创作者")
        
        # 限制数量，但确保有足够的候选
        creators = creators[:max_creators]
        
        # 3. 增强数据（获取详细信息和视频数据）
        enhanced_creators = []
        video_data_list = []
        
        for i, creator in enumerate(creators, 1):
            logger.info(f"📊 处理创作者 {i}/{len(creators)}: {creator.get('nickname', 'Unknown')}")
            
            try:
                enhanced = self.enhance_creator_data(creator)
                
                # 过滤粉丝数低于1000的创作者
                follower_count = enhanced.get("follower_count", 0)
                if follower_count < 1000:
                    logger.info(f"跳过创作者 {enhanced.get('nickname', 'Unknown')} - 粉丝数不足1000 ({follower_count})")
                    continue
                
                # 计算最新3个视频的平均播放数
                video_1_count = enhanced.get("video_1_play_count", 0)
                video_2_count = enhanced.get("video_2_play_count", 0)
                video_3_count = enhanced.get("video_3_play_count", 0)
                
                video_counts = [video_1_count, video_2_count, video_3_count]
                # 只计算有播放数据的视频
                valid_counts = [count for count in video_counts if count > 0]
                avg_play_count = sum(valid_counts) / len(valid_counts) if valid_counts else 0
                
                # 提取邮箱
                bio_description = enhanced.get("signature", "")
                email = self._extract_email_from_bio(bio_description)
                if not email:  # 确保空字符串而不是None
                    email = ""
                
                # 获取活跃度信息
                days_since_last_video = enhanced.get("days_since_last_video", -1)
                
                # 合并的完整数据（基本信息 + 视频数据 + 新增字段）
                complete_info = {
                    "search_keyword": keyword,
                    "nickname": enhanced.get("nickname", ""),
                    "unique_id": enhanced.get("unique_id", ""),
                    "follower_count": follower_count,
                    "total_video_count": enhanced.get("aweme_count", 0),
                    "total_likes_count": enhanced.get("total_favorited", 0),
                    "avg_video_play_count": int(avg_play_count),  # 移到这里
                    "days_since_last_video": days_since_last_video,  # 移到这里
                    "tiktok_account_url": enhanced.get("tiktok_account_url", ""),
                    "tiktok_account_bio_description": bio_description,
                    "email": email,  # 邮箱字段
                    "latest_video_link": enhanced.get("video_1_link", ""),
                    "latest_video_play_count": video_1_count,
                    "second_latest_video_link": enhanced.get("video_2_link", ""),
                    "second_latest_video_play_count": video_2_count,
                    "third_latest_video_link": enhanced.get("video_3_link", ""),
                    "third_latest_video_play_count": video_3_count
                }
                enhanced_creators.append(complete_info)
                
            except Exception as e:
                logger.error(f"处理创作者 {creator.get('nickname', 'Unknown')} 时出错: {e}")
                continue
        
        logger.info(f"✅ 成功收集 {len(enhanced_creators)} 个创作者的完整数据")
        return enhanced_creators, []  # 现在只返回合并的数据，第二个列表为空

if __name__ == "__main__":
    client = ComprehensiveSearchClient()
    
    # 测试
    creators, videos = client.search_and_collect_creators("ChatGPT", max_creators=5)
    
    print(f"收集到 {len(creators)} 个创作者基本信息")
    print(f"收集到 {len(videos)} 个创作者视频数据")
    
    if creators:
        print("\n示例创作者:")
        print(json.dumps(creators[0], indent=2, ensure_ascii=False))