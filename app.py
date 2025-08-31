#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikHub Web API - 为前端提供数据接口
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging
import requests
import time
import re
from config import TIKHUB_API_KEY, TIKHUB_BASE_URL

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 配置
API_KEY = TIKHUB_API_KEY
BASE_URL = TIKHUB_BASE_URL

# API请求头
API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Beee-Media-Web/1.0"
}

@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    return send_from_directory('.', filename)

@app.route('/api/trends', methods=['POST'])
def get_trends():
    """获取趋势数据"""
    try:
        data = request.get_json()
        countries = data.get('countries', [])
        
        if not countries:
            return jsonify({'error': '请选择至少一个国家'}), 400
        
        all_trends = []
        
        for country in countries:
            try:
                trends = fetch_country_trends(country)
                if trends:
                    # 添加国家信息
                    for trend in trends:
                        trend['country'] = country
                        trend['country_name'] = get_country_name(country)
                    all_trends.extend(trends)
                
                # 添加延迟避免请求过快
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"获取{country}趋势数据失败: {e}")
                continue
        
        return jsonify({
            'success': True,
            'data': all_trends,
            'total': len(all_trends),
            'countries': countries,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"获取趋势数据失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/creators/search', methods=['POST'])
def search_creators():
    """搜索创作者数据 - 调用真实的TikHub API"""
    try:
        data = request.get_json()
        search_keyword = data.get('searchKeyword', '').strip()
        country = data.get('country', '')
        follower_range = data.get('followerRange', '')
        language = data.get('language', '')
        video_count = data.get('videoCount', '')
        days_since_last_video = data.get('daysSinceLastVideo', '')
        avg_play_count = data.get('avgPlayCount', '')
        
        if not search_keyword:
            return jsonify({'error': '请输入搜索关键词'}), 400
        
        logger.info(f"🔍 搜索创作者: {search_keyword}")
        
        # 调用TikHub综合搜索API
        creators = search_creators_from_tikhub(
            search_keyword, 
            country=country,
            follower_range=follower_range,
            language=language,
            video_count=video_count,
            days_since_last_video=days_since_last_video,
            avg_play_count=avg_play_count
        )
        
        return jsonify({
            'success': True,
            'data': creators,
            'total': len(creators),
            'keyword': search_keyword,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"搜索创作者失败: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/countries', methods=['GET'])
def get_countries():
    """获取支持的国家列表"""
    countries = [
        {'code': 'UnitedStates', 'name': '美国', 'flag': '🇺🇸'},
        {'code': 'China', 'name': '中国', 'flag': '🇨🇳'},
        {'code': 'India', 'name': '印度', 'flag': '🇮🇳'},
        {'code': 'Japan', 'name': '日本', 'flag': '🇯🇵'},
        {'code': 'Russia', 'name': '俄罗斯', 'flag': '🇷🇺'},
        {'code': 'Germany', 'name': '德国', 'flag': '🇩🇪'},
        {'code': 'Indonesia', 'name': '印尼', 'flag': '🇮🇩'},
        {'code': 'Brazil', 'name': '巴西', 'flag': '🇧🇷'},
        {'code': 'France', 'name': '法国', 'flag': '🇫🇷'},
        {'code': 'UnitedKingdom', 'name': '英国', 'flag': '🇬🇧'},
        {'code': 'Turkey', 'name': '土耳其', 'flag': '🇹🇷'},
        {'code': 'Italy', 'name': '意大利', 'flag': '🇮🇹'},
        {'code': 'Mexico', 'name': '墨西哥', 'flag': '🇲🇽'},
        {'code': 'SouthKorea', 'name': '韩国', 'flag': '🇰🇷'},
        {'code': 'Canada', 'name': '加拿大', 'flag': '🇨🇦'},
        {'code': 'Spain', 'name': '西班牙', 'flag': '🇪🇸'},
        {'code': 'SaudiArabia', 'name': '沙特阿拉伯', 'flag': '🇸🇦'},
        {'code': 'Egypt', 'name': '埃及', 'flag': '🇪🇬'},
        {'code': 'Australia', 'name': '澳大利亚', 'flag': '🇦🇺'},
        {'code': 'Poland', 'name': '波兰', 'flag': '🇵🇱'},
        {'code': 'Iran', 'name': '伊朗', 'flag': '🇮🇷'},
        {'code': 'Pakistan', 'name': '巴基斯坦', 'flag': '🇵🇰'},
        {'code': 'Vietnam', 'name': '越南', 'flag': '🇻🇳'},
        {'code': 'Nigeria', 'name': '尼日利亚', 'flag': '🇳🇬'},
        {'code': 'Bangladesh', 'name': '孟加拉国', 'flag': '🇧🇩'},
        {'code': 'Netherlands', 'name': '荷兰', 'flag': '🇳🇱'},
        {'code': 'Argentina', 'name': '阿根廷', 'flag': '🇦🇷'},
        {'code': 'Philippines', 'name': '菲律宾', 'flag': '🇵🇭'},
        {'code': 'Malaysia', 'name': '马来西亚', 'flag': '🇲🇾'},
        {'code': 'Colombia', 'name': '哥伦比亚', 'flag': '🇨🇴'},
        {'code': 'UniteArabEmirates', 'name': '阿联酋', 'flag': '🇦🇪'},
        {'code': 'Romania', 'name': '罗马尼亚', 'flag': '🇷🇴'},
        {'code': 'Belgium', 'name': '比利时', 'flag': '🇧🇪'},
        {'code': 'Switzerland', 'name': '瑞士', 'flag': '🇨🇭'},
        {'code': 'Singapore', 'name': '新加坡', 'flag': '🇸🇬'},
        {'code': 'Sweden', 'name': '瑞典', 'flag': '🇸🇪'},
        {'code': 'Norway', 'name': '挪威', 'flag': '🇳🇴'},
        {'code': 'Austria', 'name': '奥地利', 'flag': '🇦🇹'},
        {'code': 'Kazakhstan', 'name': '哈萨克斯坦', 'flag': '🇰🇿'},
        {'code': 'Algeria', 'name': '阿尔及利亚', 'flag': '🇩🇿'},
        {'code': 'Chile', 'name': '智利', 'flag': '🇨🇱'},
        {'code': 'Czechia', 'name': '捷克', 'flag': '🇨🇿'},
        {'code': 'Peru', 'name': '秘鲁', 'flag': '🇵🇪'},
        {'code': 'Iraq', 'name': '伊拉克', 'flag': '🇮🇶'},
        {'code': 'Israel', 'name': '以色列', 'flag': '🇮🇱'},
        {'code': 'Ukraine', 'name': '乌克兰', 'flag': '🇺🇦'},
        {'code': 'Denmark', 'name': '丹麦', 'flag': '🇩🇰'},
        {'code': 'Portugal', 'name': '葡萄牙', 'flag': '🇵🇹'},
        {'code': 'Hungary', 'name': '匈牙利', 'flag': '🇭🇺'},
        {'code': 'Greece', 'name': '希腊', 'flag': '🇬🇷'},
        {'code': 'Finland', 'name': '芬兰', 'flag': '🇫🇮'},
        {'code': 'NewZealand', 'name': '新西兰', 'flag': '🇳🇿'},
        {'code': 'Belarus', 'name': '白俄罗斯', 'flag': '🇧🇾'},
        {'code': 'Slovakia', 'name': '斯洛伐克', 'flag': '🇸🇰'},
        {'code': 'Serbia', 'name': '塞尔维亚', 'flag': '🇷🇸'},
        {'code': 'Lithuania', 'name': '立陶宛', 'flag': '🇱🇹'},
        {'code': 'Luxembourg', 'name': '卢森堡', 'flag': '🇱🇺'},
        {'code': 'Estonia', 'name': '爱沙尼亚', 'flag': '🇪🇪'}
    ]
    
    return jsonify({
        'success': True,
        'data': countries,
        'total': len(countries)
    })

def search_creators_from_tikhub(keyword, **filters):
    """从TikHub API搜索创作者"""
    try:
        # 调用TikHub综合搜索API
        url = f"{BASE_URL}/api/v1/tiktok/app/v3/fetch_general_search_result"
        
        params = {
            "keyword": keyword,
            "offset": 0,
            "count": 50,  # 获取更多结果用于筛选
            "sort_type": 0,  # 0-相关度排序
            "publish_time": 0  # 0-不限制时间
        }
        
        logger.info(f"🔍 调用TikHub API搜索: {keyword}")
        
        # 添加请求延迟
        time.sleep(0.5)
        
        response = requests.get(url, headers=API_HEADERS, params=params, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"TikHub API请求失败: {response.status_code} - {response.text}")
            return []
        
        result = response.json()
        logger.info(f"🔍 API原始响应结构: {list(result.keys())}")
        
        # 修复：检查data.status_code而不是result.status_code
        data = result.get("data", {})
        logger.info(f"🔍 Data部分keys: {list(data.keys()) if data else 'No data'}")
        logger.info(f"🔍 Data status_code: {data.get('status_code')}")
        
        if data.get("status_code") != 0:
            logger.error(f"TikHub API返回错误: {data.get('status_msg', 'Unknown error')}")
            return []
        items = data.get("data", [])
        logger.info(f"🔍 Items类型: {type(items)}, 长度: {len(items) if isinstance(items, list) else 'Not a list'}")
        if items and len(items) > 0:
            logger.info(f"🔍 第一个item的keys: {list(items[0].keys()) if isinstance(items[0], dict) else 'Not a dict'}")
        
        logger.info(f"📊 找到 {len(items)} 个搜索结果")
        
        # 提取创作者信息
        creators = []
        creator_map = {}  # 用于去重
        
        for item in items:
            # 只处理视频类型的内容
            if item.get("type") == 1 and "aweme_info" in item:
                aweme_info = item["aweme_info"]
                author = aweme_info.get("author", {})
                
                logger.info(f"🔍 处理视频: {aweme_info.get('aweme_id', 'unknown')}")
                
                if not author:
                    logger.info("⚠️ 跳过：没有作者信息")
                    continue
                
                # 生成唯一ID - 使用nickname作为备选
                unique_id = author.get("unique_id") or author.get("sec_uid") or author.get("nickname", "")
                if not unique_id or unique_id in creator_map:
                    continue
                
                # 获取统计数据
                statistics = aweme_info.get("statistics", {})
                
                # 获取头像和视频预览信息
                avatar_url = ""
                video_cover_url = ""
                video_play_url = ""
                
                # 提取头像URL
                if "avatar_larger" in author and author["avatar_larger"] and "url_list" in author["avatar_larger"]:
                    avatar_urls = author["avatar_larger"]["url_list"]
                    avatar_url = avatar_urls[0] if avatar_urls else ""
                elif "avatar_medium" in author and author["avatar_medium"] and "url_list" in author["avatar_medium"]:
                    avatar_urls = author["avatar_medium"]["url_list"]
                    avatar_url = avatar_urls[0] if avatar_urls else ""
                
                # 提取视频封面和播放URL
                video_info = aweme_info.get("video", {})
                if "cover" in video_info and video_info["cover"] and "url_list" in video_info["cover"]:
                    cover_urls = video_info["cover"]["url_list"]
                    video_cover_url = cover_urls[0] if cover_urls else ""
                
                if "play_addr" in video_info and video_info["play_addr"] and "url_list" in video_info["play_addr"]:
                    play_urls = video_info["play_addr"]["url_list"]
                    video_play_url = play_urls[0] if play_urls else ""
                
                # 构建创作者信息
                creator = {
                    "search_keyword": keyword,
                    "nickname": author.get("nickname", ""),
                    "unique_id": unique_id,
                    "follower_count": author.get("follower_count", 0),
                    "total_video_count": author.get("aweme_count", 0),
                    "total_likes_count": author.get("total_favorited", 0),
                    "tiktok_account_url": f"https://tiktok.com/@{author.get('unique_id', '')}",
                    "tiktok_account_bio_description": author.get("signature", ""),
                    "bio_link_url": extract_bio_link(author.get("signature", "")),
                    "language": detect_language(author.get("signature", "")),
                    "latest_video_link": f"https://tiktok.com/@{author.get('unique_id', '')}/video/{aweme_info.get('aweme_id', '')}",
                    "latest_video_play_count": statistics.get("play_count", 0),
                    "second_latest_video_link": "",
                    "second_latest_video_play_count": 0,
                    "third_latest_video_link": "",
                    "third_latest_video_play_count": 0,
                    "fourth_latest_video_link": "",
                    "fourth_latest_video_play_count": 0,
                    "fifth_latest_video_link": "",
                    "fifth_latest_video_play_count": 0,
                    "days_since_last_video": calculate_days_since_last_video(aweme_info.get("create_time", 0)),
                    "avg_video_play_count": calculate_avg_play_count(aweme_info),
                    "median_view_count": calculate_median_view_count(aweme_info),
                    "expected_price": calculate_expected_price(author.get("follower_count", 0), author.get("total_favorited", 0)),
                    "email": extract_email(author.get("signature", "")),
                    # 新增：头像和视频预览
                    "avatar_url": avatar_url,
                    "video_cover_url": video_cover_url,
                    "video_play_url": video_play_url
                }
                
                # 应用筛选条件
                if apply_filters(creator, **filters):
                    creators.append(creator)
                    creator_map[unique_id] = True
        
        logger.info(f"✅ 找到 {len(creators)} 个符合条件的创作者")
        return creators
        
    except Exception as e:
        logger.error(f"TikHub API调用失败: {e}")
        return []

def apply_filters(creator, **filters):
    """应用筛选条件"""
    try:
        # 粉丝数范围筛选
        if filters.get('follower_range'):
            follower_count = creator.get('follower_count', 0)
            range_str = filters['follower_range']
            if range_str == '0-10000' and follower_count >= 10000:
                return False
            elif range_str == '10000-100000' and (follower_count < 10000 or follower_count >= 100000):
                return False
            elif range_str == '100000-1000000' and (follower_count < 100000 or follower_count >= 1000000):
                return False
            elif range_str == '1000000-10000000' and (follower_count < 1000000 or follower_count >= 10000000):
                return False
            elif range_str == '10000000-999999999' and follower_count < 10000000:
                return False
        
        # 视频数量筛选
        if filters.get('video_count'):
            try:
                min_videos = int(filters['video_count'])
                if creator.get('total_video_count', 0) < min_videos:
                    return False
            except ValueError:
                pass
        
        # 平均播放量筛选
        if filters.get('avg_play_count'):
            try:
                min_play_count = int(filters['avg_play_count'])
                if creator.get('avg_video_play_count', 0) < min_play_count:
                    return False
            except ValueError:
                pass
        
        # 最新视频天数筛选
        if filters.get('days_since_last_video'):
            try:
                max_days = int(filters['days_since_last_video'])
                if creator.get('days_since_last_video', 0) > max_days:
                    return False
            except ValueError:
                pass
        
        return True
        
    except Exception as e:
        logger.error(f"筛选条件应用失败: {e}")
        return True

def extract_bio_link(signature):
    """从个人简介中提取链接"""
    if not signature:
        return ""
    
    # 匹配各种链接格式
    url_pattern = r'https?://[^\s]+'
    matches = re.findall(url_pattern, signature)
    return matches[0] if matches else ""

def extract_email(signature):
    """从个人简介中提取邮箱"""
    if not signature:
        return ""
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, signature)
    return matches[0] if matches else ""

def detect_language(text):
    """检测语言"""
    if not text:
        return "zh"
    
    # 简单的语言检测
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    if chinese_chars > english_chars:
        return "zh"
    elif english_chars > chinese_chars:
        return "en"
    else:
        return "zh"

def calculate_days_since_last_video(create_time):
    """计算最新视频发布天数"""
    if not create_time:
        return 0
    
    try:
        # 假设create_time是时间戳
        from datetime import datetime
        video_time = datetime.fromtimestamp(create_time)
        now = datetime.now()
        delta = now - video_time
        return delta.days
    except:
        return 0

def calculate_avg_play_count(aweme_info):
    """计算平均播放量"""
    try:
        play_count = aweme_info.get("statistics", {}).get("play_count", 0)
        return play_count
    except:
        return 0

def calculate_median_view_count(aweme_info):
    """计算中位数播放量"""
    try:
        play_count = aweme_info.get("statistics", {}).get("play_count", 0)
        return play_count
    except:
        return 0

def calculate_expected_price(follower_count, total_favorited):
    """计算预期价格"""
    try:
        # 简单的价格计算公式
        base_price = 100
        follower_factor = follower_count / 10000  # 每万粉丝
        engagement_factor = total_favorited / max(follower_count, 1)  # 互动率
        
        price = base_price + (follower_factor * 50) + (engagement_factor * 1000)
        return int(max(price, 100))  # 最低100元
    except:
        return 100

def fetch_country_trends(country_code):
    """获取单个国家的趋势数据"""
    try:
        url = f"{BASE_URL}/api/v1/twitter/web/fetch_trending"
        params = {"country": country_code}
        
        response = requests.get(url, headers=API_HEADERS, params=params, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            trends = result.get("data", {}).get("trends", [])
            return trends
        else:
            logger.error(f"获取{country_code}趋势失败: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"获取{country_code}趋势数据失败: {e}")
        return []

def get_country_name(country_code):
    """根据国家代码获取国家名称"""
    country_map = {
        'UnitedStates': '美国',
        'China': '中国',
        'India': '印度',
        'Japan': '日本',
        'Russia': '俄罗斯',
        'Germany': '德国',
        'Indonesia': '印尼',
        'Brazil': '巴西',
        'France': '法国',
        'UnitedKingdom': '英国',
        'Turkey': '土耳其',
        'Italy': '意大利',
        'Mexico': '墨西哥',
        'SouthKorea': '韩国',
        'Canada': '加拿大',
        'Spain': '西班牙',
        'SaudiArabia': '沙特阿拉伯',
        'Egypt': '埃及',
        'Australia': '澳大利亚',
        'Poland': '波兰',
        'Iran': '伊朗',
        'Pakistan': '巴基斯坦',
        'Vietnam': '越南',
        'Nigeria': '尼日利亚',
        'Bangladesh': '孟加拉国',
        'Netherlands': '荷兰',
        'Argentina': '阿根廷',
        'Philippines': '菲律宾',
        'Malaysia': '马来西亚',
        'Colombia': '哥伦比亚',
        'UniteArabEmirates': '阿联酋',
        'Romania': '罗马尼亚',
        'Belgium': '比利时',
        'Switzerland': '瑞士',
        'Singapore': '新加坡',
        'Sweden': '瑞典',
        'Norway': '挪威',
        'Austria': '奥地利',
        'Kazakhstan': '哈萨克斯坦',
        'Algeria': '阿尔及利亚',
        'Chile': '智利',
        'Czechia': '捷克',
        'Peru': '秘鲁',
        'Iraq': '伊拉克',
        'Israel': '以色列',
        'Ukraine': '乌克兰',
        'Denmark': '丹麦',
        'Portugal': '葡萄牙',
        'Hungary': '匈牙利',
        'Greece': '希腊',
        'Finland': '芬兰',
        'NewZealand': '新西兰',
        'Belarus': '白俄罗斯',
        'Slovakia': '斯洛伐克',
        'Serbia': '塞尔维亚',
        'Lithuania': '立陶宛',
        'Luxembourg': '卢森堡',
        'Estonia': '爱沙尼亚'
    }
    
    return country_map.get(country_code, country_code)

@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({'error': '页面未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    """处理500错误"""
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("🚀 TikHub Web API 启动中...")
    print(f"📊 支持的国家数量: 58")
    print(f"🔑 API密钥: {API_KEY[:10]}...")
    print(f"🌐 服务地址: http://localhost:8080")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8080)
