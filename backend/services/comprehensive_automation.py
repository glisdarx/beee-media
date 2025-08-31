#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok创作者数据收集自动化系统 - 基于综合搜索API
生成两个CSV表格：创作者基本信息 和 创作者视频数据
"""

import csv
import json
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict
from comprehensive_search_client import ComprehensiveSearchClient

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TikTokCreatorAutomation:
    """TikTok创作者数据自动化收集系统"""
    
    def __init__(self):
        self.client = ComprehensiveSearchClient()
        self.output_dir = "output"
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        import os
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def collect_creators_data(self, keywords: List[str], max_creators_per_keyword: int = 20) -> Dict:
        """
        收集多个关键词的创作者数据
        
        Args:
            keywords: 关键词列表
            max_creators_per_keyword: 每个关键词最大创作者数量
            
        Returns:
            Dict: 包含所有数据的字典
        """
        all_creators_basic = []
        all_creators_videos = []
        
        for keyword in keywords:
            logger.info(f"🔍 处理关键词: {keyword}")
            
            try:
                creators_basic, creators_videos = self.client.search_and_collect_creators(
                    keyword, max_creators=max_creators_per_keyword
                )
                
                all_creators_basic.extend(creators_basic)
                all_creators_videos.extend(creators_videos)
                
                logger.info(f"✅ 关键词 '{keyword}' 完成，收集到 {len(creators_basic)} 个创作者")
                
            except Exception as e:
                logger.error(f"处理关键词 '{keyword}' 时出错: {e}")
                continue
        
        return {
            "creators_basic": all_creators_basic,
            "creators_videos": all_creators_videos,
            "total_creators": len(all_creators_basic),
            "keywords": keywords
        }
    
    def save_to_csv(self, data: Dict, filename_prefix: str = None) -> Dict[str, str]:
        """
        保存数据到CSV文件
        
        Args:
            data: 收集的数据
            filename_prefix: 文件名前缀
            
        Returns:
            Dict[str, str]: 生成的文件路径
        """
        if not filename_prefix:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_prefix = f"tiktok_creators_{timestamp}"
        
        # 合并的完整信息CSV
        complete_file = f"{self.output_dir}/{filename_prefix}_complete.csv"
        
        # 保存合并的完整创作者信息
        if data["creators_basic"]:
            df_complete = pd.DataFrame(data["creators_basic"])
            # 将空字符串替换为实际的空字符串，避免NaN显示
            df_complete = df_complete.fillna('')
            df_complete.to_csv(complete_file, index=False, encoding='utf-8-sig')
            logger.info(f"✅ 创作者完整信息已保存到: {complete_file}")
        
        return {
            "complete_file": complete_file
        }
    
    def save_to_excel(self, data: Dict, filename_prefix: str = None) -> str:
        """
        保存数据到Excel文件
        
        Args:
            data: 收集的数据
            filename_prefix: 文件名前缀
            
        Returns:
            str: Excel文件路径
        """
        if not filename_prefix:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_prefix = f"tiktok_creators_{timestamp}"
        
        excel_file = f"{self.output_dir}/{filename_prefix}_complete.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # 完整创作者信息（包含视频数据）
            if data["creators_basic"]:
                df_complete = pd.DataFrame(data["creators_basic"])
                df_complete.to_excel(writer, sheet_name='创作者完整信息', index=False)
        
        logger.info(f"✅ 完整数据已保存到Excel: {excel_file}")
        return excel_file
    
    def save_summary_report(self, data: Dict, filename_prefix: str = None) -> str:
        """生成数据收集报告"""
        if not filename_prefix:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_prefix = f"tiktok_creators_{timestamp}"
        
        report_file = f"{self.output_dir}/{filename_prefix}_report.json"
        
        # 统计信息
        basic_stats = {}
        if data["creators_basic"]:
            df = pd.DataFrame(data["creators_basic"])
            basic_stats = {
                "total_creators": int(len(df)),
                "total_followers": int(df["follower_count"].sum()),
                "avg_followers": float(df["follower_count"].mean()),
                "total_videos": int(df["total_video_count"].sum()),
                "total_likes": int(df["total_likes_count"].sum()),
                "keywords_processed": data["keywords"],
                "top_creators_by_followers": [
                    {
                        "nickname": str(row["nickname"]),
                        "follower_count": int(row["follower_count"])
                    }
                    for _, row in df.nlargest(5, "follower_count").iterrows()
                ]
            }
        
        report = {
            "collection_time": datetime.now().isoformat(),
            "keywords": data["keywords"],
            "basic_statistics": basic_stats,
            "files_generated": {
                "creators_count": len(data["creators_basic"]),
                "note": "All data (basic info + video data) combined in single file"
            }
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ 数据报告已保存到: {report_file}")
        return report_file
    
    def run_automation(self, keywords: List[str], max_creators_per_keyword: int = 20, 
                      output_format: str = "both") -> Dict[str, str]:
        """
        运行完整的自动化流程
        
        Args:
            keywords: 关键词列表
            max_creators_per_keyword: 每个关键词最大创作者数量
            output_format: 输出格式 ("csv", "excel", "both")
            
        Returns:
            Dict[str, str]: 生成的文件路径
        """
        logger.info(f"🚀 开始TikTok创作者数据收集")
        logger.info(f"关键词: {keywords}")
        logger.info(f"每个关键词最大创作者数: {max_creators_per_keyword}")
        
        # 1. 收集数据
        data = self.collect_creators_data(keywords, max_creators_per_keyword)
        
        if not data["creators_basic"]:
            logger.warning("❌ 未收集到任何创作者数据")
            return {}
        
        # 2. 生成文件名前缀
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        keywords_str = "_".join(keywords[:3])  # 最多使用前3个关键词
        filename_prefix = f"tiktok_{keywords_str}_{timestamp}"
        
        # 3. 保存数据
        file_paths = {}
        
        if output_format in ["csv", "both"]:
            csv_files = self.save_to_csv(data, filename_prefix)
            file_paths.update(csv_files)
        
        if output_format in ["excel", "both"]:
            excel_file = self.save_to_excel(data, filename_prefix)
            file_paths["excel_file"] = excel_file
        
        # 4. 生成报告
        report_file = self.save_summary_report(data, filename_prefix)
        file_paths["report_file"] = report_file
        
        # 5. 显示结果总结
        self._print_summary(data)
        
        return file_paths
    
    def _print_summary(self, data: Dict):
        """打印收集结果总结"""
        print("\n" + "="*60)
        print("📊 TikTok创作者数据收集完成")
        print("="*60)
        print(f"🔍 搜索关键词: {', '.join(data['keywords'])}")
        print(f"👥 收集创作者数量: {len(data['creators_basic'])} (过滤了粉丝数<1000的创作者)")
        
        if data["creators_basic"]:
            df = pd.DataFrame(data["creators_basic"])
            print(f"📈 总粉丝数: {df['follower_count'].sum():,}")
            print(f"📹 总视频数: {df['total_video_count'].sum():,}")
            print(f"❤️ 总点赞数: {df['total_likes_count'].sum():,}")
            print(f"📊 平均视频播放数: {df['avg_video_play_count'].mean():,.0f}")
            
            # 活跃度统计
            active_creators = df[df['days_since_last_video'] != -1]
            if len(active_creators) > 0:
                avg_days = active_creators['days_since_last_video'].mean()
                print(f"⏰ 平均最近发布天数: {avg_days:.1f} 天")
            
            # 邮箱统计
            email_count = df[df['email'] != ''].shape[0]
            print(f"📧 包含邮箱的创作者: {email_count} 个 ({email_count/len(df)*100:.1f}%)")
            
            print(f"\n🏆 Top 5 创作者 (按粉丝数):")
            top_creators = df.nlargest(5, "follower_count")
            for i, creator in top_creators.iterrows():
                avg_views = creator.get('avg_video_play_count', 0)
                days_since = creator.get('days_since_last_video', -1)
                email_info = " | 📧" if creator.get('email', '') else ""
                activity_info = f" | {days_since}天前" if days_since != -1 else " | 活跃度未知"
                print(f"  {creator['nickname']} (@{creator['unique_id']}) - {creator['follower_count']:,} 粉丝 | 平均播放: {avg_views:,}{activity_info}{email_info}")
        
        print("="*60)

def main():
    """主函数 - 交互式运行"""
    automation = TikTokCreatorAutomation()
    
    print("🚀 TikTok创作者数据收集自动化系统")
    print("="*50)
    
    # 获取用户输入
    keywords_input = input("请输入搜索关键词（用逗号分隔）: ").strip()
    keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
    
    if not keywords:
        print("❌ 请至少输入一个关键词")
        return
    
    try:
        max_creators = int(input("每个关键词最大创作者数量（默认20）: ") or "20")
    except ValueError:
        max_creators = 20
    
    output_format = input("输出格式 (csv/excel/both，默认both): ").strip().lower() or "both"
    
    # 运行自动化
    try:
        file_paths = automation.run_automation(keywords, max_creators, output_format)
        
        if file_paths:
            print(f"\n✅ 文件已生成:")
            for file_type, file_path in file_paths.items():
                print(f"  {file_type}: {file_path}")
        else:
            print("❌ 未生成任何文件")
            
    except KeyboardInterrupt:
        print("\n❌ 用户中断执行")
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        logger.error(f"执行出错: {e}", exc_info=True)

if __name__ == "__main__":
    main()