"""
Supabase 数据库客户端
处理所有数据库操作
"""

import os
from typing import Optional, Dict, List, Any
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            logger.warning("SUPABASE_URL or SUPABASE_ANON_KEY not set, database functionality will be disabled")
            self.client = None
        else:
            self.client: Client = create_client(self.url, self.key)
            logger.info("Supabase client initialized")
    
    # 用户管理
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict]:
        """创建新用户"""
        if not self.client:
            logger.warning("Supabase client not initialized, cannot create user")
            return None
            
        try:
            result = self.client.table('users').insert(user_data).execute()
            if result.data:
                logger.info(f"User created successfully: {user_data.get('email')}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """通过邮箱获取用户"""
        if not self.client:
            logger.warning("Supabase client not initialized, cannot get user")
            return None
            
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    async def get_user_by_google_id(self, google_id: str) -> Optional[Dict]:
        """通过Google ID获取用户"""
        try:
            result = self.client.table('users').select('*').eq('google_id', google_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by Google ID: {e}")
            return None
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        """更新用户信息"""
        try:
            result = self.client.table('users').update(update_data).eq('id', user_id).execute()
            if result.data:
                logger.info(f"User updated successfully: {user_id}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return None
    
    async def update_last_login(self, user_id: str) -> bool:
        """更新用户最后登录时间"""
        try:
            result = self.client.table('users').update({
                'last_login': 'NOW()'
            }).eq('id', user_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False
    
    # 搜索历史管理
    async def save_search_history(self, user_id: str, search_data: Dict[str, Any]) -> Optional[Dict]:
        """保存搜索历史"""
        try:
            search_record = {
                'user_id': user_id,
                'search_query': search_data.get('query', ''),
                'search_type': search_data.get('type', 'creators'),
                'filters': search_data.get('filters', {}),
                'results_count': search_data.get('results_count', 0),
                'results_data': search_data.get('results_data')
            }
            
            result = self.client.table('search_history').insert(search_record).execute()
            if result.data:
                logger.info(f"Search history saved for user: {user_id}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error saving search history: {e}")
            return None
    
    async def get_user_search_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """获取用户搜索历史"""
        try:
            result = self.client.table('search_history') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .limit(limit) \
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting search history: {e}")
            return []
    
    # 收藏管理
    async def add_favorite_creator(self, user_id: str, creator_data: Dict[str, Any]) -> Optional[Dict]:
        """添加收藏的创作者"""
        try:
            favorite_record = {
                'user_id': user_id,
                'creator_unique_id': creator_data.get('unique_id'),
                'creator_nickname': creator_data.get('nickname'),
                'creator_data': creator_data,
                'notes': creator_data.get('notes', ''),
                'tags': creator_data.get('tags', [])
            }
            
            result = self.client.table('favorite_creators').insert(favorite_record).execute()
            if result.data:
                logger.info(f"Creator favorited: {creator_data.get('unique_id')} by user: {user_id}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error adding favorite creator: {e}")
            return None
    
    async def remove_favorite_creator(self, user_id: str, creator_unique_id: str) -> bool:
        """移除收藏的创作者"""
        try:
            result = self.client.table('favorite_creators') \
                .delete() \
                .eq('user_id', user_id) \
                .eq('creator_unique_id', creator_unique_id) \
                .execute()
            
            logger.info(f"Creator unfavorited: {creator_unique_id} by user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing favorite creator: {e}")
            return False
    
    async def get_user_favorites(self, user_id: str) -> List[Dict]:
        """获取用户收藏的创作者"""
        try:
            result = self.client.table('favorite_creators') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .execute()
            
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting user favorites: {e}")
            return []
    
    async def is_creator_favorited(self, user_id: str, creator_unique_id: str) -> bool:
        """检查创作者是否已被收藏"""
        try:
            result = self.client.table('favorite_creators') \
                .select('id') \
                .eq('user_id', user_id) \
                .eq('creator_unique_id', creator_unique_id) \
                .execute()
            
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error checking if creator is favorited: {e}")
            return False
    
    # API使用统计
    async def log_api_usage(self, user_id: str, endpoint: str, method: str, 
                           response_status: int, response_time_ms: int, 
                           ip_address: str = None) -> bool:
        """记录API使用"""
        try:
            usage_record = {
                'user_id': user_id,
                'endpoint': endpoint,
                'method': method,
                'response_status': response_status,
                'response_time_ms': response_time_ms,
                'ip_address': ip_address
            }
            
            result = self.client.table('api_usage_logs').insert(usage_record).execute()
            
            # 更新用户的API使用计数
            await self.increment_user_api_usage(user_id)
            
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error logging API usage: {e}")
            return False
    
    async def increment_user_api_usage(self, user_id: str) -> bool:
        """增加用户API使用计数"""
        try:
            # 获取当前计数
            user = await self.get_user_by_id(user_id)
            if user:
                new_count = user.get('api_usage_count', 0) + 1
                await self.update_user(user_id, {'api_usage_count': new_count})
            return True
        except Exception as e:
            logger.error(f"Error incrementing API usage: {e}")
            return False
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """通过ID获取用户"""
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    async def check_api_usage_limit(self, user_id: str) -> Dict[str, Any]:
        """检查用户API使用限制"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return {'allowed': False, 'reason': 'User not found'}
            
            usage_count = user.get('api_usage_count', 0)
            usage_limit = user.get('api_usage_limit', 100)
            
            if usage_count >= usage_limit:
                return {
                    'allowed': False, 
                    'reason': 'API usage limit exceeded',
                    'usage_count': usage_count,
                    'usage_limit': usage_limit
                }
            
            return {
                'allowed': True,
                'usage_count': usage_count,
                'usage_limit': usage_limit,
                'remaining': usage_limit - usage_count
            }
        except Exception as e:
            logger.error(f"Error checking API usage limit: {e}")
            return {'allowed': False, 'reason': 'Error checking limits'}
    
    # 邮件日志
    async def log_email_sent(self, email_data: Dict[str, Any]) -> Optional[Dict]:
        """记录邮件发送"""
        try:
            result = self.client.table('email_logs').insert(email_data).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error logging email: {e}")
            return None

# 创建全局实例
db_client = SupabaseClient()
