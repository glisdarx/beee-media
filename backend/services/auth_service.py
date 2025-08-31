"""
认证服务
处理用户注册、登录、JWT token管理
"""

import os
import jwt
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from google.auth.transport import requests
from google.oauth2 import id_token
import bcrypt

from .supabase_client import db_client
from .sendgrid_client import email_client

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-this')
        self.jwt_algorithm = 'HS256'
        self.jwt_expiration_hours = 24
        self.google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        
        if not self.google_client_id:
            logger.warning("GOOGLE_CLIENT_ID not set, Google OAuth will not work")
        
        logger.info("Auth service initialized")
    
    def generate_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """生成JWT token"""
        payload = {
            'user_id': user_data['id'],
            'email': user_data['email'],
            'name': user_data['name'],
            'subscription_tier': user_data.get('subscription_tier', 'free'),
            'exp': datetime.utcnow() + timedelta(hours=self.jwt_expiration_hours),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        logger.info(f"JWT token generated for user: {user_data['email']}")
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """验证JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
    
    def hash_password(self, password: str) -> str:
        """加密密码"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def generate_verification_token(self) -> str:
        """生成验证token"""
        return secrets.token_urlsafe(32)
    
    async def register_with_email(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """邮箱注册"""
        try:
            # 检查邮箱是否已存在
            existing_user = await db_client.get_user_by_email(email)
            if existing_user:
                return {
                    'success': False,
                    'error': 'Email already registered',
                    'message': '该邮箱已被注册'
                }
            
            # 创建用户
            verification_token = self.generate_verification_token()
            hashed_password = self.hash_password(password)
            
            user_data = {
                'email': email,
                'name': name,
                'password_hash': hashed_password,
                'verification_token': verification_token,
                'email_verified': False,
                'subscription_tier': 'free',
                'api_usage_count': 0,
                'api_usage_limit': 100
            }
            
            new_user = await db_client.create_user(user_data)
            if not new_user:
                return {
                    'success': False,
                    'error': 'Failed to create user',
                    'message': '创建用户失败'
                }
            
            # 发送验证邮件
            verification_link = f"https://beeemedia.com/verify-email?token={verification_token}"
            email_result = await email_client.send_verification_email(
                email, name, verification_link
            )
            
            # 记录邮件发送日志
            await db_client.log_email_sent({
                'user_id': new_user['id'],
                'recipient_email': email,
                'template_name': 'email_verification',
                'subject': '请验证您的 Beee Media 账户邮箱',
                'status': 'sent' if email_result.get('success') else 'failed',
                'sendgrid_message_id': email_result.get('message_id'),
                'error_message': email_result.get('error') if not email_result.get('success') else None,
                'sent_at': datetime.utcnow() if email_result.get('success') else None
            })
            
            return {
                'success': True,
                'message': '注册成功！请检查您的邮箱并点击验证链接。',
                'user_id': new_user['id'],
                'email_sent': email_result.get('success', False)
            }
            
        except Exception as e:
            logger.error(f"Error in email registration: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '注册过程中发生错误'
            }
    
    async def login_with_email(self, email: str, password: str) -> Dict[str, Any]:
        """邮箱登录"""
        try:
            # 获取用户
            user = await db_client.get_user_by_email(email)
            if not user:
                return {
                    'success': False,
                    'error': 'User not found',
                    'message': '用户不存在'
                }
            
            # 检查密码
            if not user.get('password_hash'):
                return {
                    'success': False,
                    'error': 'Password not set',
                    'message': '该账户使用Google登录，请使用Google登录方式'
                }
            
            if not self.verify_password(password, user['password_hash']):
                return {
                    'success': False,
                    'error': 'Invalid password',
                    'message': '密码错误'
                }
            
            # 检查邮箱是否已验证
            if not user.get('email_verified', False):
                return {
                    'success': False,
                    'error': 'Email not verified',
                    'message': '请先验证您的邮箱地址'
                }
            
            # 检查账户是否激活
            if not user.get('is_active', True):
                return {
                    'success': False,
                    'error': 'Account deactivated',
                    'message': '账户已被停用'
                }
            
            # 更新最后登录时间
            await db_client.update_last_login(user['id'])
            
            # 生成JWT token
            token = self.generate_jwt_token(user)
            
            return {
                'success': True,
                'message': '登录成功',
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'avatar_url': user.get('avatar_url'),
                    'subscription_tier': user.get('subscription_tier', 'free')
                }
            }
            
        except Exception as e:
            logger.error(f"Error in email login: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '登录过程中发生错误'
            }
    
    async def login_with_google(self, google_token: str) -> Dict[str, Any]:
        """Google OAuth登录"""
        try:
            # 验证Google token
            idinfo = id_token.verify_oauth2_token(
                google_token, requests.Request(), self.google_client_id
            )
            
            google_user_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo['name']
            avatar_url = idinfo.get('picture')
            
            # 检查用户是否已存在
            user = await db_client.get_user_by_google_id(google_user_id)
            
            if not user:
                # 检查邮箱是否已被其他方式注册
                existing_user = await db_client.get_user_by_email(email)
                if existing_user:
                    # 更新现有用户的Google ID
                    user = await db_client.update_user(existing_user['id'], {
                        'google_id': google_user_id,
                        'avatar_url': avatar_url,
                        'email_verified': True  # Google账户默认已验证
                    })
                else:
                    # 创建新用户
                    user_data = {
                        'email': email,
                        'google_id': google_user_id,
                        'name': name,
                        'avatar_url': avatar_url,
                        'email_verified': True,
                        'subscription_tier': 'free',
                        'api_usage_count': 0,
                        'api_usage_limit': 100
                    }
                    
                    user = await db_client.create_user(user_data)
                    
                    if user:
                        # 发送欢迎邮件
                        email_result = await email_client.send_welcome_email(email, name)
                        
                        # 记录邮件发送日志
                        await db_client.log_email_sent({
                            'user_id': user['id'],
                            'recipient_email': email,
                            'template_name': 'welcome_email',
                            'subject': f'欢迎加入 Beee Media, {name}! 🎉',
                            'status': 'sent' if email_result.get('success') else 'failed',
                            'sendgrid_message_id': email_result.get('message_id'),
                            'error_message': email_result.get('error') if not email_result.get('success') else None,
                            'sent_at': datetime.utcnow() if email_result.get('success') else None
                        })
            
            if not user:
                return {
                    'success': False,
                    'error': 'Failed to create or retrieve user',
                    'message': '用户创建或获取失败'
                }
            
            # 检查账户是否激活
            if not user.get('is_active', True):
                return {
                    'success': False,
                    'error': 'Account deactivated',
                    'message': '账户已被停用'
                }
            
            # 更新最后登录时间和头像
            await db_client.update_user(user['id'], {
                'last_login': datetime.utcnow().isoformat(),
                'avatar_url': avatar_url  # 更新最新头像
            })
            
            # 生成JWT token
            token = self.generate_jwt_token(user)
            
            return {
                'success': True,
                'message': '登录成功',
                'token': token,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name'],
                    'avatar_url': user.get('avatar_url'),
                    'subscription_tier': user.get('subscription_tier', 'free')
                }
            }
            
        except ValueError as e:
            logger.error(f"Invalid Google token: {e}")
            return {
                'success': False,
                'error': 'Invalid Google token',
                'message': 'Google登录验证失败'
            }
        except Exception as e:
            logger.error(f"Error in Google login: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Google登录过程中发生错误'
            }
    
    async def verify_email(self, verification_token: str) -> Dict[str, Any]:
        """验证邮箱"""
        try:
            # 查找具有此验证token的用户
            result = db_client.client.table('users').select('*').eq('verification_token', verification_token).execute()
            
            if not result.data:
                return {
                    'success': False,
                    'error': 'Invalid verification token',
                    'message': '验证链接无效或已过期'
                }
            
            user = result.data[0]
            
            if user.get('email_verified', False):
                return {
                    'success': False,
                    'error': 'Email already verified',
                    'message': '邮箱已经验证过了'
                }
            
            # 更新用户验证状态
            updated_user = await db_client.update_user(user['id'], {
                'email_verified': True,
                'verification_token': None  # 清除验证token
            })
            
            if updated_user:
                # 发送欢迎邮件
                email_result = await email_client.send_welcome_email(
                    user['email'], user['name']
                )
                
                # 记录邮件发送日志
                await db_client.log_email_sent({
                    'user_id': user['id'],
                    'recipient_email': user['email'],
                    'template_name': 'welcome_email',
                    'subject': f'欢迎加入 Beee Media, {user["name"]}! 🎉',
                    'status': 'sent' if email_result.get('success') else 'failed',
                    'sendgrid_message_id': email_result.get('message_id'),
                    'error_message': email_result.get('error') if not email_result.get('success') else None,
                    'sent_at': datetime.utcnow() if email_result.get('success') else None
                })
                
                return {
                    'success': True,
                    'message': '邮箱验证成功！欢迎加入 Beee Media！'
                }
            
            return {
                'success': False,
                'error': 'Failed to update user',
                'message': '验证过程中发生错误'
            }
            
        except Exception as e:
            logger.error(f"Error in email verification: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '邮箱验证过程中发生错误'
            }
    
    async def request_password_reset(self, email: str) -> Dict[str, Any]:
        """请求密码重置"""
        try:
            user = await db_client.get_user_by_email(email)
            if not user:
                # 为了安全，即使用户不存在也返回成功消息
                return {
                    'success': True,
                    'message': '如果该邮箱存在，我们已发送密码重置链接'
                }
            
            # 生成重置token
            reset_token = self.generate_verification_token()
            
            # 更新用户的重置token
            await db_client.update_user(user['id'], {
                'verification_token': reset_token
            })
            
            # 发送密码重置邮件
            reset_link = f"https://beeemedia.com/reset-password?token={reset_token}"
            email_result = await email_client.send_password_reset_email(
                email, user['name'], reset_link
            )
            
            # 记录邮件发送日志
            await db_client.log_email_sent({
                'user_id': user['id'],
                'recipient_email': email,
                'template_name': 'password_reset',
                'subject': '重置您的 Beee Media 密码',
                'status': 'sent' if email_result.get('success') else 'failed',
                'sendgrid_message_id': email_result.get('message_id'),
                'error_message': email_result.get('error') if not email_result.get('success') else None,
                'sent_at': datetime.utcnow() if email_result.get('success') else None
            })
            
            return {
                'success': True,
                'message': '密码重置链接已发送到您的邮箱'
            }
            
        except Exception as e:
            logger.error(f"Error in password reset request: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '密码重置请求过程中发生错误'
            }
    
    async def reset_password(self, reset_token: str, new_password: str) -> Dict[str, Any]:
        """重置密码"""
        try:
            # 查找具有此重置token的用户
            result = db_client.client.table('users').select('*').eq('verification_token', reset_token).execute()
            
            if not result.data:
                return {
                    'success': False,
                    'error': 'Invalid reset token',
                    'message': '重置链接无效或已过期'
                }
            
            user = result.data[0]
            
            # 加密新密码
            hashed_password = self.hash_password(new_password)
            
            # 更新用户密码并清除重置token
            updated_user = await db_client.update_user(user['id'], {
                'password_hash': hashed_password,
                'verification_token': None
            })
            
            if updated_user:
                return {
                    'success': True,
                    'message': '密码重置成功！请使用新密码登录。'
                }
            
            return {
                'success': False,
                'error': 'Failed to update password',
                'message': '密码重置过程中发生错误'
            }
            
        except Exception as e:
            logger.error(f"Error in password reset: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '密码重置过程中发生错误'
            }

# 创建全局实例
auth_service = AuthService()
