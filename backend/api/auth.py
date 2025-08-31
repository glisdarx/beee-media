"""
认证相关API路由
"""

from flask import Blueprint, request, jsonify
import asyncio
import logging
from functools import wraps

from services.auth_service import auth_service
from services.supabase_client import db_client

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def async_route(f):
    """装饰器：让Flask路由支持异步函数"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

def jwt_required(f):
    """装饰器：要求JWT认证"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            payload = auth_service.verify_jwt_token(token)
            if not payload:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            request.current_user = payload
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"JWT verification error: {e}")
            return jsonify({'error': 'Token verification failed'}), 401
    
    return wrapper

@auth_bp.route('/register', methods=['POST'])
@async_route
async def register():
    """邮箱注册"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 基本验证
        email = data['email'].strip().lower()
        password = data['password']
        name = data['name'].strip()
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password too short',
                'message': '密码长度至少6位'
            }), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email format',
                'message': '邮箱格式无效'
            }), 400
        
        # 调用认证服务
        result = await auth_service.register_with_email(email, password, name)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '注册过程中发生错误'
        }), 500

@auth_bp.route('/login', methods=['POST'])
@async_route
async def login():
    """邮箱登录"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Missing email or password',
                'message': '邮箱和密码都是必需的'
            }), 400
        
        # 调用认证服务
        result = await auth_service.login_with_email(email, password)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '登录过程中发生错误'
        }), 500

@auth_bp.route('/google-login', methods=['POST'])
@async_route
async def google_login():
    """Google OAuth登录"""
    try:
        data = request.get_json()
        google_token = data.get('google_token')
        
        if not google_token:
            return jsonify({
                'success': False,
                'error': 'Missing Google token',
                'message': '缺少Google令牌'
            }), 400
        
        # 调用认证服务
        result = await auth_service.login_with_google(google_token)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in Google login endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Google登录过程中发生错误'
        }), 500

@auth_bp.route('/verify-email', methods=['POST'])
@async_route
async def verify_email():
    """邮箱验证"""
    try:
        data = request.get_json()
        verification_token = data.get('token')
        
        if not verification_token:
            return jsonify({
                'success': False,
                'error': 'Missing verification token',
                'message': '缺少验证令牌'
            }), 400
        
        # 调用认证服务
        result = await auth_service.verify_email(verification_token)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in email verification endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '邮箱验证过程中发生错误'
        }), 500

@auth_bp.route('/forgot-password', methods=['POST'])
@async_route
async def forgot_password():
    """忘记密码"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({
                'success': False,
                'error': 'Missing email',
                'message': '邮箱地址是必需的'
            }), 400
        
        # 调用认证服务
        result = await auth_service.request_password_reset(email)
        
        # 始终返回成功消息（安全考虑）
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in forgot password endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '密码重置请求过程中发生错误'
        }), 500

@auth_bp.route('/reset-password', methods=['POST'])
@async_route
async def reset_password():
    """重置密码"""
    try:
        data = request.get_json()
        reset_token = data.get('token')
        new_password = data.get('password')
        
        if not reset_token or not new_password:
            return jsonify({
                'success': False,
                'error': 'Missing token or password',
                'message': '缺少重置令牌或新密码'
            }), 400
        
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password too short',
                'message': '密码长度至少6位'
            }), 400
        
        # 调用认证服务
        result = await auth_service.reset_password(reset_token, new_password)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in reset password endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '密码重置过程中发生错误'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required
@async_route
async def get_profile():
    """获取用户资料"""
    try:
        user_id = request.current_user['user_id']
        user = await db_client.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'message': '用户不存在'
            }), 404
        
        # 返回用户信息（不包含敏感信息）
        profile = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'avatar_url': user.get('avatar_url'),
            'subscription_tier': user.get('subscription_tier', 'free'),
            'api_usage_count': user.get('api_usage_count', 0),
            'api_usage_limit': user.get('api_usage_limit', 100),
            'email_verified': user.get('email_verified', False),
            'created_at': user.get('created_at'),
            'last_login': user.get('last_login')
        }
        
        return jsonify({
            'success': True,
            'user': profile
        }), 200
        
    except Exception as e:
        logger.error(f"Error in profile endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取用户资料时发生错误'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required
@async_route
async def update_profile():
    """更新用户资料"""
    try:
        user_id = request.current_user['user_id']
        data = request.get_json()
        
        # 允许更新的字段
        allowed_fields = ['name', 'avatar_url']
        update_data = {}
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if not update_data:
            return jsonify({
                'success': False,
                'error': 'No valid fields to update',
                'message': '没有可更新的字段'
            }), 400
        
        # 更新用户信息
        updated_user = await db_client.update_user(user_id, update_data)
        
        if not updated_user:
            return jsonify({
                'success': False,
                'error': 'Failed to update user',
                'message': '更新用户信息失败'
            }), 500
        
        return jsonify({
            'success': True,
            'message': '用户资料更新成功',
            'user': {
                'id': updated_user['id'],
                'email': updated_user['email'],
                'name': updated_user['name'],
                'avatar_url': updated_user.get('avatar_url')
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in update profile endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '更新用户资料时发生错误'
        }), 500

@auth_bp.route('/check-usage', methods=['GET'])
@jwt_required
@async_route
async def check_api_usage():
    """检查API使用限制"""
    try:
        user_id = request.current_user['user_id']
        usage_info = await db_client.check_api_usage_limit(user_id)
        
        return jsonify({
            'success': True,
            'usage': usage_info
        }), 200
        
    except Exception as e:
        logger.error(f"Error in check usage endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '检查API使用情况时发生错误'
        }), 500
