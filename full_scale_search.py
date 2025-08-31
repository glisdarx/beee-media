#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全量TikTok创作者搜索系统
支持上千次搜索，去重优化，基于官方配置
"""

import time
import json
import logging
import math
import os
from datetime import datetime
from typing import Dict, List, Set, Optional
from comprehensive_search_client import ComprehensiveSearchClient
from comprehensive_automation import TikTokCreatorAutomation
import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FullScaleSearchEngine:
    """全量搜索引擎"""
    
    def __init__(self):
        self.client = ComprehensiveSearchClient()
        self.automation = TikTokCreatorAutomation()
        
        # 去重和缓存
        self.seen_creator_ids: Set[str] = set()
        self.seen_video_ids: Set[str] = set()
        self.collected_creators: List[Dict] = []
        
        # 搜索配置 - 基于官方配置优化
        self.qps_limit = 10  # 每秒10次请求
        self.request_interval = 0.1  # 100ms间隔，支持10 QPS
        self.max_retries = 3
        self.timeout = 45  # 45秒超时
        
        # 分页搜索配置
        self.max_per_search = 30  # 每次搜索30个，保证稳定性
        self.max_offset = 10000  # 最大偏移量，支持深度搜索
        
        # 文件编号管理
        self.next_file_number = self._get_next_file_number()
    
    def _get_next_file_number(self) -> int:
        """获取下一个文件编号"""
        if not os.path.exists("output"):
            return 1
        
        existing_numbers = []
        for filename in os.listdir("output"):
            # 匹配格式：数字_关键词_时间戳.csv 或 数字_关键词_时间戳_report.json
            if filename.endswith('.csv') or filename.endswith('_report.json'):
                parts = filename.split('_')
                if len(parts) >= 2:
                    try:
                        number = int(parts[0])
                        existing_numbers.append(number)
                    except ValueError:
                        continue
        
        if not existing_numbers:
            return 1
        
        return max(existing_numbers) + 1
        
    def full_scale_search(self, keyword: str, target_creators: int = 1000) -> List[Dict]:
        """
        全量搜索指定关键词
        
        Args:
            keyword: 搜索关键词
            target_creators: 目标创作者数量
            
        Returns:
            List[Dict]: 去重后的创作者列表
        """
        logger.info(f"🚀 开始全量搜索关键词: '{keyword}', 目标: {target_creators} 个创作者")
        
        all_videos = []
        search_count = 0
        offset = 0
        consecutive_empty = 0
        
        while len(self.collected_creators) < target_creators and offset < self.max_offset:
            search_count += 1
            
            logger.info(f"📦 搜索批次 {search_count}, offset={offset}, 已收集={len(self.collected_creators)}")
            
            # 执行分页搜索
            videos = self._paginated_search(keyword, offset=offset, count=self.max_per_search)
            
            if not videos:
                consecutive_empty += 1
                logger.warning(f"空结果 {consecutive_empty}/3")
                
                if consecutive_empty >= 3:
                    logger.warning("连续3次空结果，可能已达搜索极限")
                    break
                    
                # 空结果时，跳跃更大的偏移量
                offset += self.max_per_search * 2
                continue
            else:
                consecutive_empty = 0
                
            # 去重新视频
            new_videos = self._deduplicate_videos(videos)
            all_videos.extend(new_videos)
            
            logger.info(f"本批次: {len(videos)} 个视频, 去重后: {len(new_videos)} 个新视频")
            
            # 提取和去重创作者
            new_creators = self._extract_and_deduplicate_creators(new_videos)
            self.collected_creators.extend(new_creators)
            
            # 如果超过目标数量，截取前N个（按粉丝数排序）
            if len(self.collected_creators) > target_creators:
                logger.info(f"🎯 达到目标数量，截取前 {target_creators} 个创作者")
                self.collected_creators = sorted(self.collected_creators, 
                                               key=lambda x: x.get('follower_count', 0), 
                                               reverse=True)[:target_creators]
                break
            
            logger.info(f"累计视频: {len(all_videos)}, 累计创作者: {len(self.collected_creators)}")
            
            # 更新偏移量
            offset += self.max_per_search
            
            # 速率限制
            time.sleep(self.request_interval)
            
            # 每100次搜索保存一次中间结果
            if search_count % 100 == 0:
                self._save_intermediate_results(keyword, search_count)
        
        logger.info(f"✅ 全量搜索完成: {search_count} 次搜索, {len(all_videos)} 个视频, {len(self.collected_creators)} 个唯一创作者")
        return self.collected_creators
    
    def _paginated_search(self, keyword: str, offset: int = 0, count: int = 30) -> List[Dict]:
        """执行分页搜索"""
        url = f"{self.client.base_url}/api/v1/tiktok/app/v3/fetch_general_search_result"
        
        params = {
            "keyword": keyword,
            "offset": offset,
            "count": count,
            "sort_type": 0,
            "publish_time": 0
        }
        
        # 使用重试机制
        for attempt in range(self.max_retries):
            try:
                result = self.client._make_request(url, params)
                if result:
                    data = result.get("data", {})
                    items = data.get("data", [])
                    
                    videos = []
                    for item in items:
                        if item.get("type") == 1 and "aweme_info" in item:
                            videos.append(item["aweme_info"])
                    
                    return videos
                else:
                    logger.warning(f"搜索失败，尝试 {attempt + 1}/{self.max_retries}")
                    time.sleep(2 ** attempt)  # 指数退避
                    
            except Exception as e:
                logger.error(f"搜索异常 {attempt + 1}/{self.max_retries}: {e}")
                time.sleep(2 ** attempt)
        
        return []
    
    def _deduplicate_videos(self, videos: List[Dict]) -> List[Dict]:
        """去重视频"""
        new_videos = []
        for video in videos:
            video_id = video.get("aweme_id", "")
            if video_id and video_id not in self.seen_video_ids:
                self.seen_video_ids.add(video_id)
                new_videos.append(video)
        return new_videos
    
    def _extract_and_deduplicate_creators(self, videos: List[Dict]) -> List[Dict]:
        """提取并去重创作者"""
        new_creators = []
        
        for video in videos:
            author = video.get("author", {})
            if not author:
                continue
            
            # 多重去重键
            unique_id = author.get("unique_id", "")
            user_id = author.get("uid", "")
            sec_uid = author.get("sec_uid", "")
            
            # 生成去重键
            creator_key = unique_id or user_id or sec_uid
            if not creator_key or creator_key in self.seen_creator_ids:
                continue
            
            # 粉丝数过滤
            follower_count = author.get("follower_count", 0)
            if follower_count < 1000:
                continue
            
            self.seen_creator_ids.add(creator_key)
            
            # 提取创作者基本信息
            creator_info = {
                "user_id": user_id,
                "sec_user_id": sec_uid,
                "nickname": author.get("nickname", ""),
                "unique_id": unique_id,
                "signature": author.get("signature", ""),
                "follower_count": follower_count,
                "following_count": author.get("following_count", 0),
                "aweme_count": author.get("aweme_count", 0),
                "total_favorited": author.get("total_favorited", 0),
                "avatar_url": author.get("avatar_larger", {}).get("url_list", [""])[0] if author.get("avatar_larger") else "",
                "verified": author.get("verification_type", 0) > 0,
                "tiktok_account_url": self.client._generate_tiktok_url(unique_id)
            }
            
            new_creators.append(creator_info)
        
        return new_creators
    
    def _save_intermediate_results(self, keyword: str, search_count: int):
        """保存中间结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/intermediate_{keyword}_{search_count}_{timestamp}.json"
        
        data = {
            "keyword": keyword,
            "search_count": search_count,
            "total_creators": len(self.collected_creators),
            "total_videos": len(self.seen_video_ids),
            "creators": self.collected_creators
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"💾 中间结果已保存: {filename}")
        except Exception as e:
            logger.error(f"保存中间结果失败: {e}")
    
    def enhance_creators_batch(self, creators: List[Dict], batch_size: int = 50) -> List[Dict]:
        """批量增强创作者数据"""
        logger.info(f"🔧 开始批量增强 {len(creators)} 个创作者的数据")
        
        enhanced_creators = []
        
        for i in range(0, len(creators), batch_size):
            batch = creators[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(creators) + batch_size - 1) // batch_size
            
            logger.info(f"📦 处理批次 {batch_num}/{total_batches} ({len(batch)} 个创作者)")
            
            for j, creator in enumerate(batch, 1):
                try:
                    logger.info(f"📊 增强创作者 {i+j}/{len(creators)}: {creator.get('nickname', 'Unknown')}")
                    enhanced = self.client.enhance_creator_data(creator)
                    
                    if enhanced:
                        # 应用字段顺序和数据处理
                        processed = self._process_creator_data(enhanced)
                        enhanced_creators.append(processed)
                    
                except Exception as e:
                    logger.error(f"增强创作者数据失败: {e}")
                    continue
            
            # 批次间休息
            if batch_num < total_batches:
                logger.info(f"⏳ 批次完成，休息1秒...")
                time.sleep(1)
        
        logger.info(f"✅ 批量增强完成: {len(enhanced_creators)}/{len(creators)} 成功")
        return enhanced_creators
    
    def _process_creator_data(self, enhanced: Dict) -> Dict:
        """处理创作者数据，应用字段顺序"""
        # 计算平均播放数
        video_1_count = enhanced.get("video_1_play_count", 0)
        video_2_count = enhanced.get("video_2_play_count", 0)
        video_3_count = enhanced.get("video_3_play_count", 0)
        video_4_count = enhanced.get("video_4_play_count", 0)
        video_5_count = enhanced.get("video_5_play_count", 0)
        
        video_counts = [video_1_count, video_2_count, video_3_count, video_4_count, video_5_count]
        valid_counts = [count for count in video_counts if count > 0]
        avg_play_count = sum(valid_counts) / len(valid_counts) if valid_counts else 0
        
        # 计算中位数播放量
        if valid_counts:
            sorted_counts = sorted(valid_counts)
            n = len(sorted_counts)
            if n % 2 == 0:
                # 偶数个数，取中间两个数的平均值
                median_view_count = (sorted_counts[n//2 - 1] + sorted_counts[n//2]) / 2
            else:
                # 奇数个数，取中间的数
                median_view_count = sorted_counts[n//2]
        else:
            median_view_count = 0
        
        # 计算预期价格: 使用新的复杂公式
        # weighted_views = 0.4 * V1 + 0.25 * V2 + 0.15 * V3 + 0.1 * V4 + 0.1 * V5
        weights = [0.4, 0.25, 0.15, 0.1, 0.1]
        weighted_views = 0
        for i, count in enumerate([video_1_count, video_2_count, video_3_count, video_4_count, video_5_count]):
            if i < len(weights) and count > 0:
                weighted_views += weights[i] * count
        
        # follower_factor = log10(follower_count + 1)
        follower_count = enhanced.get("follower_count", 0)
        follower_factor = math.log10(follower_count + 1) if follower_count >= 0 else 0
        
        # engagement_rate = (total_likes_count / total_video_count) / avg_video_play_count
        total_likes = enhanced.get("total_favorited", 0)
        total_videos = enhanced.get("aweme_count", 1)  # 避免除零
        if total_videos > 0 and avg_play_count > 0:
            engagement_rate = (total_likes / total_videos) / avg_play_count
        else:
            engagement_rate = 0
        
        # final_price = max(80, weighted_views/1000 * 1 + follower_factor * 5 + engagement_rate * 50)
        calculated_price = (weighted_views / 1000) * 1 + follower_factor * 5 + engagement_rate * 50
        expected_price = max(80, calculated_price)
        
        # 提取邮箱
        bio_description = enhanced.get("signature", "")
        email = self.client._extract_email_from_bio(bio_description)
        if not email:
            email = ""
        
        # 获取活跃度
        days_since_last_video = enhanced.get("days_since_last_video", -1)
        
        # 按要求的字段顺序
        return {
            "search_keyword": "temp",  # 后续会更新
            "nickname": enhanced.get("nickname", ""),
            "unique_id": enhanced.get("unique_id", ""),
            "follower_count": enhanced.get("follower_count", 0),
            "total_video_count": enhanced.get("aweme_count", 0),
            "total_likes_count": enhanced.get("total_favorited", 0),
            "avg_video_play_count": int(avg_play_count),
            "median_view_count": int(median_view_count),
            "expected_price": round(expected_price, 2),
            "days_since_last_video": days_since_last_video,
            "tiktok_account_url": enhanced.get("tiktok_account_url", ""),
            "tiktok_account_bio_description": bio_description,
            "email": email,
            "bio_link_url": enhanced.get("bio_link_url", ""),
            "language": enhanced.get("language", ""),
            "latest_video_link": enhanced.get("video_1_link", ""),
            "latest_video_play_count": video_1_count,
            "second_latest_video_link": enhanced.get("video_2_link", ""),
            "second_latest_video_play_count": video_2_count,
            "third_latest_video_link": enhanced.get("video_3_link", ""),
            "third_latest_video_play_count": video_3_count,
            "fourth_latest_video_link": enhanced.get("video_4_link", ""),
            "fourth_latest_video_play_count": video_4_count,
            "fifth_latest_video_link": enhanced.get("video_5_link", ""),
            "fifth_latest_video_play_count": video_5_count
        }
    
    def save_results(self, keyword: str, enhanced_creators: List[Dict], output_format: str = "csv", keyword_index: int = 1) -> Dict[str, str]:
        """保存最终结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 使用动态文件编号，基于现有文件自动递增
        file_number = self.next_file_number
        self.next_file_number += 1  # 为下一个文件准备编号
        file_prefix = f"output/{file_number:02d}_{keyword}_{timestamp}"
        
        # 更新search_keyword字段
        for creator in enhanced_creators:
            creator["search_keyword"] = keyword
        
        file_paths = {}
        
        # 保存CSV
        if output_format in ["csv", "both"]:
            csv_file = f"{file_prefix}.csv"
            df = pd.DataFrame(enhanced_creators)
            df = df.fillna('')  # 处理NaN值
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
            file_paths["csv_file"] = csv_file
            logger.info(f"✅ CSV文件已保存: {csv_file}")
        
        # 保存Excel
        if output_format in ["excel", "both"]:
            excel_file = f"{file_prefix}.xlsx"
            df = pd.DataFrame(enhanced_creators)
            df = df.fillna('')
            df.to_excel(excel_file, index=False, sheet_name='创作者完整信息')
            file_paths["excel_file"] = excel_file
            logger.info(f"✅ Excel文件已保存: {excel_file}")
        
        # 保存统计报告
        report_file = f"{file_prefix}_report.json"
        report = self._generate_report(keyword, enhanced_creators)
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        file_paths["report_file"] = report_file
        
        return file_paths
    
    def _generate_report(self, keyword: str, creators: List[Dict]) -> Dict:
        """生成统计报告"""
        if not creators:
            return {"error": "无数据"}
        
        df = pd.DataFrame(creators)
        
        return {
            "keyword": keyword,
            "collection_time": datetime.now().isoformat(),
            "total_searches": len(self.seen_video_ids),
            "total_creators": len(creators),
            "total_followers": int(df["follower_count"].sum()),
            "avg_followers": float(df["follower_count"].mean()),
            "total_videos": int(df["total_video_count"].sum()),
            "total_likes": int(df["total_likes_count"].sum()),
            "avg_play_count": float(df["avg_video_play_count"].mean()),
            "email_count": len(df[df["email"] != ""]),
            "active_creators": len(df[df["days_since_last_video"] <= 30]),
            "top_creators": [
                {
                    "nickname": str(row["nickname"]),
                    "unique_id": str(row["unique_id"]),
                    "follower_count": int(row["follower_count"])
                }
                for _, row in df.nlargest(10, "follower_count").iterrows()
            ]
        }

def process_single_keyword(engine, keyword: str, target_creators: int, enhance_data: bool, output_format: str) -> dict:
    """处理单个关键词的搜索"""
    print(f"\n🔍 开始搜索关键词: '{keyword}'")
    print(f"目标数量: {target_creators} | 增强数据: {'是' if enhance_data else '否'}")
    print("-" * 50)
    
    start_time = time.time()
    
    # 重置引擎状态（清空之前的收集结果）
    engine.seen_creator_ids.clear()
    engine.seen_video_ids.clear()
    engine.collected_creators.clear()
    
    # 第一阶段：全量搜索
    print("📦 第一阶段: 全量搜索创作者...")
    raw_creators = engine.full_scale_search(keyword, target_creators)
    
    if not raw_creators:
        print(f"❌ 关键词 '{keyword}' 未找到任何创作者")
        return {"keyword": keyword, "success": False, "creators": [], "file_paths": {}, "time": 0}
    
    phase1_time = time.time() - start_time
    print(f"✅ 第一阶段完成: {len(raw_creators)} 个创作者, 用时 {phase1_time/60:.1f} 分钟")
    
    # 第二阶段：数据增强
    if enhance_data:
        print(f"📊 第二阶段: 数据增强...")
        enhanced_creators = engine.enhance_creators_batch(raw_creators)
    else:
        # 不增强数据，直接处理
        enhanced_creators = []
        for creator in raw_creators:
            processed = engine._process_creator_data(creator)
            enhanced_creators.append(processed)
    
    total_time = time.time() - start_time
    
    # 确保精确数量控制
    if len(enhanced_creators) > target_creators:
        print(f"⚡ 数量控制: 从 {len(enhanced_creators)} 个减少到 {target_creators} 个")
        print(f"📊 排序方式: 按粉丝数降序排列，取前 {target_creators} 名")
        enhanced_creators = sorted(enhanced_creators, 
                                 key=lambda x: x.get('follower_count', 0), 
                                 reverse=True)[:target_creators]
    
    # 保存结果
    file_paths = engine.save_results(keyword, enhanced_creators, output_format)
    
    # 显示结果
    print(f"✅ 关键词 '{keyword}' 搜索完成!")
    print(f"⏱️ 用时: {total_time/60:.1f} 分钟")
    print(f"📊 结果: {len(enhanced_creators)} 个创作者")
    
    if enhanced_creators:
        df = pd.DataFrame(enhanced_creators)
        print(f"📈 统计: 平均粉丝 {df['follower_count'].mean():,.0f} | 邮箱 {len(df[df['email'] != ''])} 个")
    
    return {
        "keyword": keyword,
        "success": True,
        "creators": enhanced_creators,
        "file_paths": file_paths,
        "time": total_time
    }

def main():
    """主函数"""
    print("🚀 TikTok全量创作者搜索系统")
    print("支持多关键词搜索，智能去重，基于官方配置优化")
    print("="*70)
    
    engine = FullScaleSearchEngine()
    
    try:
        # 获取搜索参数
        keywords_input = input("请输入搜索关键词(多个用逗号分隔): ").strip()
        if not keywords_input:
            print("❌ 请输入有效关键词")
            return
        
        # 解析多个关键词，处理空格
        keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
        if not keywords:
            print("❌ 请输入有效关键词")
            return
        
        print(f"📝 解析到 {len(keywords)} 个关键词: {keywords}")
        
        try:
            target_creators = int(input("每个关键词的目标创作者数量（默认20）: ") or "20")
        except ValueError:
            target_creators = 20
        
        output_format = input("输出格式 (csv/excel/both，默认csv): ").strip().lower() or "csv"
        
        # 是否增强数据
        enhance_choice = input("是否获取详细视频数据? (会显著增加时间) (y/n，默认y): ").strip().lower() or "y"
        enhance_data = enhance_choice in ['y', 'yes', '是']
        
        print(f"\n🎯 搜索配置:")
        print(f"关键词数量: {len(keywords)}")
        print(f"每个关键词目标: {target_creators} 个创作者")
        print(f"增强数据: {'是' if enhance_data else '否'}")
        print(f"输出格式: {output_format}")
        print(f"配置: QPS=10, 重试=3次, 超时=45s")
        print("="*70)
        
        overall_start_time = time.time()
        all_results = []
        total_creators = 0
        
        # 逐个处理关键词
        for i, keyword in enumerate(keywords, 1):
            print(f"\n🚀 处理关键词 {i}/{len(keywords)}: '{keyword}'")
            
            result = process_single_keyword(engine, keyword, target_creators, enhance_data, output_format)
            all_results.append(result)
            
            if result["success"]:
                total_creators += len(result["creators"])
                print(f"📁 生成文件:")
                for file_type, path in result["file_paths"].items():
                    print(f"  📄 {file_type}: {path}")
            
            # 关键词间休息（除了最后一个）
            if i < len(keywords):
                print(f"⏳ 准备处理下一个关键词...")
                time.sleep(2)
        
        overall_time = time.time() - overall_start_time
        
        # 总结报告
        print(f"\n🎉 多关键词搜索完成!")
        print(f"⏱️ 总用时: {overall_time/60:.1f} 分钟")
        print(f"📊 总体结果:")
        print(f"  • 处理关键词: {len(keywords)} 个")
        print(f"  • 成功关键词: {sum(1 for r in all_results if r['success'])} 个")
        print(f"  • 总创作者数: {total_creators} 个")
        print(f"  • 平均每个关键词: {total_creators/len(keywords):.1f} 个")
        
        # 显示每个关键词的结果
        print(f"\n📋 详细结果:")
        for result in all_results:
            status = "✅" if result["success"] else "❌"
            creators_count = len(result["creators"]) if result["success"] else 0
            print(f"  {status} '{result['keyword']}': {creators_count} 个创作者")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ 用户中断执行")
        if hasattr(engine, 'collected_creators') and engine.collected_creators:
            print(f"💾 保存已收集的 {len(engine.collected_creators)} 个创作者...")
    except Exception as e:
        print(f"\n❌ 程序出错: {e}")
        logger.error(f"程序出错: {e}", exc_info=True)

if __name__ == "__main__":
    main()