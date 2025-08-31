"""
Beee Media 主应用文件
集成用户认证、TikHub API和前端服务
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import asyncio

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 导入服务和配置
from config.config import get_config
from services.supabase_client import db_client
from services.sendgrid_client import email_client
from services.auth_service import auth_service
from api.auth import auth_bp, jwt_required

# 导入现有的TikHub功能
import sys
sys.path.append('services')
from services.comprehensive_search_client import ComprehensiveSearchClient

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 加载配置
config = get_config()
app.config.from_object(config)

# 设置CORS
CORS(app, origins=config.CORS_ORIGINS)

# 设置速率限制
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATELIMIT_DEFAULT]
)

# 注册蓝图
app.register_blueprint(auth_bp)

# 创建TikHub客户端
tikhub_client = ComprehensiveSearchClient()

# ================================
# 静态文件服务
# ================================

@app.route('/')
def index():
    """主页"""
    return send_from_directory('../frontend/pages', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """服务静态文件"""
    # 尝试从不同目录提供文件
    try:
        if filename.endswith('.html'):
            return send_from_directory('../frontend/pages', filename)
        elif filename.endswith('.css'):
            return send_from_directory('../frontend/assets/css', filename)
        elif filename.endswith('.js'):
            return send_from_directory('../frontend/assets/js', filename)
        elif filename.endswith(('.ico', '.png', '.jpg', '.svg')):
            return send_from_directory('../frontend/assets/icons', filename)
        else:
            return send_from_directory('../frontend', filename)
    except Exception as e:
        logger.error(f"静态文件未找到: {filename}, 错误: {e}")
        return jsonify({'error': 'File not found'}), 404

# ================================
# API中间件
# ================================

@app.before_request
def before_request():
    """请求前处理"""
    # 记录请求
    logger.info(f"{request.method} {request.path} - {get_remote_address()}")
    
    # 为API请求添加开始时间
    if request.path.startswith('/api/'):
        request.start_time = datetime.utcnow()

@app.after_request
def after_request(response):
    """请求后处理"""
    # 记录API使用情况
    if request.path.startswith('/api/') and hasattr(request, 'start_time'):
        response_time = (datetime.utcnow() - request.start_time).total_seconds() * 1000
        
        # 如果是认证用户，记录API使用
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = auth_service.verify_jwt_token(token)
                if payload:
                    asyncio.create_task(db_client.log_api_usage(
                        user_id=payload['user_id'],
                        endpoint=request.path,
                        method=request.method,
                        response_status=response.status_code,
                        response_time_ms=int(response_time),
                        ip_address=get_remote_address()
                    ))
            except:
                pass  # 忽略token验证错误
    
    return response

# ================================
# TikHub API 端点
# ================================

@app.route('/api/creators/search', methods=['POST'])
@limiter.limit("30 per minute")
async def search_creators():
    """搜索创作者（公开API，无需认证）"""
    try:
        # 公开API，无需认证
        user_id = 'anonymous'

        data = request.get_json()
        keyword = data.get('keyword', '')
        country = data.get('country', 'US')
        region = data.get('region', '')
        min_followers = data.get('min_followers', 0)
        max_followers = data.get('max_followers', 10000000)
        
        if not keyword:
            return jsonify({
                'success': False,
                'error': 'Missing keyword',
                'message': '请输入搜索关键词'
            }), 400
        
        logger.info(f"🔍 用户 {user_id} 搜索创作者: {keyword}")
        
        # 调用TikHub API
        search_results = await search_creators_from_tikhub(
            keyword, country, region, min_followers, max_followers
        )
        
        if search_results['success']:
            # 保存搜索历史（如果数据库可用）
            try:
                await db_client.save_search_history(user_id, {
                    'query': keyword,
                    'type': 'creators',
                    'filters': {
                        'country': country,
                        'region': region,
                        'min_followers': min_followers,
                        'max_followers': max_followers
                    },
                    'results_count': len(search_results['data']),
                    'results_data': search_results['data'][:5]  # 只保存前5个结果作为快照
                })
            except:
                pass  # 数据库不可用时忽略
            
            logger.info(f"✅ 找到 {len(search_results['data'])} 个创作者")
        
        return jsonify(search_results)
        
    except Exception as e:
        logger.error(f"搜索创作者时发生错误: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '搜索过程中发生错误'
        }), 500

async def search_creators_from_tikhub(keyword, country='US', region='', min_followers=0, max_followers=10000000):
    """调用TikHub API搜索创作者"""
    try:
        logger.info(f"🔍 调用TikHub API搜索: {keyword}")
        
        # 调用TikHub comprehensive_search API
        search_params = {
            'keyword': keyword,
            'count': 20,
            'sort_type': 1
        }
        
        videos = tikhub_client.comprehensive_search(**search_params)
        
        if not videos:
            logger.error("TikHub API返回空数据")
            return {
                'success': False,
                'error': 'TikHub API error',
                'message': 'API调用失败',
                'data': [],
                'total': 0
            }
        
        # 提取创作者信息
        creators_data = []
        
        logger.info(f"📊 找到 {len(videos)} 个搜索结果")
        
        unique_creators = {}
        
        for video in videos:
            # 根据实际API结构，author和statistics直接在顶层
            author = video.get("author", {})
            statistics = video.get("statistics", {})
            
            unique_id = author.get("unique_id", "")
            if not unique_id or unique_id in unique_creators:
                continue
                
            # 获取粉丝数
            follower_count = author.get("follower_count", 0)
            
            # 应用粉丝数过滤
            if follower_count < min_followers or follower_count > max_followers:
                continue
            
            # 提取创作者信息
            creator_info = {
                'search_keyword': keyword,
                'nickname': author.get("nickname", ""),
                'unique_id': unique_id,
                'follower_count': follower_count,
                'total_video_count': author.get("aweme_count", 0),
                'total_likes_count': author.get("total_favorited", 0),
                'tiktok_account_url': f"https://www.tiktok.com/@{unique_id}",
                'tiktok_account_bio_description': author.get("signature", ""),
                'bio_link_url': extract_bio_link(author.get("signature", "")),
                'language': detect_language(author.get("signature", "")),
                'avatar_url': author.get("avatar_larger", {}).get("url_list", [""])[0] if author.get("avatar_larger") else "",
                
                # 视频信息
                'latest_video_link': f"https://www.tiktok.com/@{unique_id}/video/{video.get('aweme_id', '')}",
                'latest_video_play_count': statistics.get("play_count", 0),
                'video_cover_url': video.get("video", {}).get("cover", {}).get("url_list", [""])[0] if video.get("video") else "",
                'video_play_url': video.get("video", {}).get("play_addr", {}).get("url_list", [""])[0] if video.get("video") else "",
                
                # 计算字段
                'days_since_last_video': calculate_days_since_last_video(video.get("create_time", 0)),
                'avg_video_play_count': statistics.get("play_count", 0),  # 当前视频的播放量
                'median_view_count': statistics.get("play_count", 0),    # 当前视频的播放量
                'expected_price': calculate_expected_price(follower_count, statistics.get("play_count", 0)),
                'email': extract_email_from_bio(author.get("signature", ""))
            }
            
            unique_creators[unique_id] = creator_info
            creators_data.append(creator_info)
        
        logger.info(f"✅ 找到 {len(creators_data)} 个符合条件的创作者")
        
        return {
            'success': True,
            'data': creators_data,
            'total': len(creators_data),
            'message': f'找到 {len(creators_data)} 个创作者'
        }
        
    except Exception as e:
        logger.error(f"TikHub API调用失败: {e}")
        return {
            'success': False,
            'error': str(e),
            'message': 'API调用过程中发生错误',
            'data': [],
            'total': 0
        }

def calculate_expected_price(follower_count, avg_play_count):
    """计算预期价格"""
    # 简单的价格计算公式
    base_price = follower_count * 0.001  # 每个粉丝0.001元
    engagement_bonus = avg_play_count * 0.0001  # 播放量奖励
    return round(base_price + engagement_bonus, 2)

def extract_email_from_bio(bio):
    """从简介中提取邮箱"""
    import re
    if not bio:
        return ""
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, bio)
    return matches[0] if matches else ""

def extract_bio_link(bio_text):
    """从个人简介中提取链接"""
    if not bio_text:
        return ""
    
    # 提取各种链接格式
    link_patterns = [
        r'https?://[^\s]+',
        r'linktr\.ee/[^\s]+',
        r'bio\.link/[^\s]+',
        r'beacons\.ai/[^\s]+'
    ]
    
    for pattern in link_patterns:
        match = re.search(pattern, bio_text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return ""

def detect_language(text):
    """检测文本语言"""
    if not text:
        return "en"
    
    # 简单的语言检测
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    if chinese_chars > english_chars:
        return "zh-CN"
    else:
        return "en"

def calculate_days_since_last_video(create_time):
    """计算距离最新视频发布的天数"""
    if not create_time:
        return 0
    
    try:
        # 时间戳是毫秒，需要转换为秒
        video_time = datetime.fromtimestamp(create_time / 1000)
        current_time = datetime.now()
        days_diff = (current_time - video_time).days
        return max(0, days_diff)
    except:
        return 0

# ================================
# 用户收藏功能
# ================================

@app.route('/api/creators/favorites', methods=['GET'])
@jwt_required
async def get_user_favorites():
    """获取用户收藏的创作者"""
    try:
        user_id = request.current_user['user_id']
        favorites = await db_client.get_user_favorites(user_id)
        
        return jsonify({
            'success': True,
            'data': favorites,
            'total': len(favorites)
        })
        
    except Exception as e:
        logger.error(f"获取收藏列表失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取收藏列表失败'
        }), 500

@app.route('/api/creators/favorites', methods=['POST'])
@jwt_required
async def add_favorite_creator():
    """添加收藏的创作者"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        creator_data = data.get('creator')
        if not creator_data or not creator_data.get('unique_id'):
            return jsonify({
                'success': False,
                'error': 'Invalid creator data',
                'message': '创作者数据无效'
            }), 400
        
        # 检查是否已收藏
        is_favorited = await db_client.is_creator_favorited(
            user_id, creator_data['unique_id']
        )
        
        if is_favorited:
            return jsonify({
                'success': False,
                'error': 'Already favorited',
                'message': '该创作者已在收藏列表中'
            }), 400
        
        # 添加收藏
        favorite = await db_client.add_favorite_creator(user_id, creator_data)
        
        if favorite:
            return jsonify({
                'success': True,
                'message': '收藏成功',
                'data': favorite
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add favorite',
                'message': '收藏失败'
            }), 500
            
    except Exception as e:
        logger.error(f"添加收藏失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '添加收藏失败'
        }), 500

@app.route('/api/creators/favorites/<creator_unique_id>', methods=['DELETE'])
@jwt_required
async def remove_favorite_creator(creator_unique_id):
    """移除收藏的创作者"""
    try:
        user_id = request.current_user['user_id']
        
        success = await db_client.remove_favorite_creator(user_id, creator_unique_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '取消收藏成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to remove favorite',
                'message': '取消收藏失败'
            }), 500
            
    except Exception as e:
        logger.error(f"取消收藏失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '取消收藏失败'
        }), 500

# ================================
# 搜索历史功能
# ================================

@app.route('/api/search/history', methods=['GET'])
@jwt_required
async def get_search_history():
    """获取用户搜索历史"""
    try:
        user_id = request.current_user['user_id']
        limit = request.args.get('limit', 50, type=int)
        
        history = await db_client.get_user_search_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'data': history,
            'total': len(history)
        })
        
    except Exception as e:
        logger.error(f"获取搜索历史失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取搜索历史失败'
        }), 500

# ================================
# 趋势数据API (保持原有功能)
# ================================

@app.route('/api/trends', methods=['GET'])
@limiter.limit("20 per minute")
def get_trends():
    """获取趋势数据（无需认证）"""
    # 这里保持原有的趋势获取逻辑
    return jsonify({
        'success': True,
        'data': [],
        'message': '趋势功能暂时不可用'
    })

# ================================
# 健康检查和配置
# ================================

@app.route('/api/health')
def health_check():
    """健康检查"""
    config_validation = config.validate_config()
    
    return jsonify({
        'status': 'healthy' if config_validation['valid'] else 'warning',
        'timestamp': datetime.utcnow().isoformat(),
        'config': config.get_config_summary(),
        'validation': config_validation
    })

@app.route('/api/config')
def get_public_config():
    """获取公开配置"""
    return jsonify({
        'google_client_id': config.GOOGLE_CLIENT_ID,
        'features': {
            'google_oauth': bool(config.GOOGLE_CLIENT_ID),
            'email_auth': bool(config.SENDGRID_API_KEY),
            'tikhub_search': bool(config.TIKHUB_API_KEY)
        }
    })

# ================================
# 错误处理
# ================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': '请求过于频繁，请稍后再试'
    }), 429

# ================================
# 应用启动
# ================================

if __name__ == '__main__':
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    # 验证配置
    config_validation = config.validate_config()
    if not config_validation['valid']:
        logger.error("配置验证失败:")
        for error in config_validation['errors']:
            logger.error(f"  - {error}")
        exit(1)
    
    if config_validation['warnings']:
        logger.warning("配置警告:")
        for warning in config_validation['warnings']:
            logger.warning(f"  - {warning}")
    
    logger.info("🚀 Beee Media API 启动中...")
    logger.info(f"🔑 认证系统: {'✅' if config.GOOGLE_CLIENT_ID or config.SENDGRID_API_KEY else '❌'}")
    logger.info(f"📧 邮箱服务: {'✅' if config.SENDGRID_API_KEY else '❌'}")
    logger.info(f"🗄️ 数据库: {'✅' if config.SUPABASE_URL else '❌'}")
    logger.info(f"🔍 TikHub API: {'✅' if config.TIKHUB_API_KEY else '❌'}")
    logger.info("=" * 50)
    
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=config.DEBUG,
        threaded=True
    )