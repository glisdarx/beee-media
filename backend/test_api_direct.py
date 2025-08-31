#!/usr/bin/env python3
"""
直接测试API逻辑，绕过认证
"""

import os
import sys
import asyncio
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv('../.env')

from services.comprehensive_search_client import ComprehensiveSearchClient

async def test_api_direct():
    """直接测试API逻辑"""
    print("🧪 开始直接测试API逻辑...")
    
    # 创建TikHub客户端
    client = ComprehensiveSearchClient()
    
    # 测试搜索
    keyword = "food"
    print(f"🔍 搜索关键词: {keyword}")
    
    try:
        # 直接调用搜索方法
        videos = client.comprehensive_search(keyword=keyword, count=5, sort_type=1)
        
        if not videos:
            print("❌ 没有找到视频数据")
            return
        
        print(f"✅ 找到 {len(videos)} 个视频")
        
        # 提取创作者信息
        creators = client.extract_creators_from_videos(videos)
        
        if not creators:
            print("❌ 没有找到创作者数据")
            return
        
        print(f"✅ 找到 {len(creators)} 个创作者")
        
        # 显示第一个创作者的详细信息
        if creators:
            creator = creators[0]
            print("\n📋 第一个创作者信息:")
            print(f"昵称: {creator.get('nickname', 'N/A')}")
            print(f"唯一ID: {creator.get('unique_id', 'N/A')}")
            print(f"粉丝数: {creator.get('follower_count', 0):,}")
            print(f"视频数: {creator.get('aweme_count', 0)}")
            print(f"总点赞: {creator.get('total_favorited', 0):,}")
            print(f"TikTok链接: {creator.get('tiktok_account_url', 'N/A')}")
            print(f"头像: {creator.get('avatar_url', 'N/A')[:50]}...")
            
            # 测试获取用户详细资料
            unique_id = creator.get('unique_id')
            if unique_id:
                print(f"\n🔍 获取用户详细资料: {unique_id}")
                profile = client.get_user_profile_web(unique_id=unique_id)
                if profile:
                    print("✅ 成功获取用户详细资料")
                    print(f"个人简介: {profile.get('signature', 'N/A')[:100]}...")
                else:
                    print("❌ 获取用户详细资料失败")
        
        return creators
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 运行测试
    result = asyncio.run(test_api_direct())
    
    if result:
        print(f"\n🎉 测试成功！找到 {len(result)} 个创作者")
    else:
        print("\n❌ 测试失败")
