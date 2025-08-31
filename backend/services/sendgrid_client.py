"""
SendGrid 邮箱服务客户端
处理所有邮件发送功能
"""

import os
import logging
from typing import Dict, List, Optional, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import json

logger = logging.getLogger(__name__)

class SendGridClient:
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@beeemedia.com')
        self.from_name = os.getenv('SENDGRID_FROM_NAME', 'Beee Media')
        
        if not self.api_key:
            logger.warning("SENDGRID_API_KEY not set, email functionality will be disabled")
            self.client = None
        else:
            self.client = SendGridAPIClient(api_key=self.api_key)
            logger.info("SendGrid client initialized")
    
    async def send_email(self, to_email: str, subject: str, 
                        html_content: str, text_content: str = None,
                        template_id: str = None, dynamic_data: Dict = None) -> Dict[str, Any]:
        """发送邮件"""
        if not self.client:
            logger.warning("SendGrid client not initialized, email not sent")
            return {
                'success': False,
                'error': 'SendGrid not configured',
                'message': 'Email service not available'
            }
        
        try:
            from_email = Email(self.from_email, self.from_name)
            to_email_obj = To(to_email)
            
            if template_id:
                # 使用 SendGrid 模板
                mail = Mail(
                    from_email=from_email,
                    to_emails=to_email_obj,
                    subject=subject
                )
                mail.template_id = template_id
                
                if dynamic_data:
                    mail.dynamic_template_data = dynamic_data
            else:
                # 使用自定义内容
                content = Content("text/html", html_content)
                mail = Mail(from_email, to_email_obj, subject, content)
                
                if text_content:
                    mail.add_content(Content("text/plain", text_content))
            
            response = self.client.send(mail)
            
            result = {
                'success': True,
                'status_code': response.status_code,
                'message_id': response.headers.get('X-Message-Id'),
                'response_body': response.body
            }
            
            logger.info(f"Email sent successfully to {to_email}, Message ID: {result['message_id']}")
            return result
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> Dict[str, Any]:
        """发送欢迎邮件"""
        subject = f"欢迎加入 Beee Media, {user_name}! 🎉"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>欢迎加入 Beee Media</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #FFA500); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .button {{ display: inline-block; background: #FFD700; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🐝 欢迎加入 Beee Media!</h1>
                </div>
                <div class="content">
                    <h2>你好, {user_name}!</h2>
                    <p>感谢您加入 Beee Media - 您的AI驱动营销增长伙伴！</p>
                    
                    <h3>🚀 您现在可以:</h3>
                    <ul>
                        <li>🔍 搜索和分析TikTok创作者</li>
                        <li>📊 获取实时趋势数据</li>
                        <li>💾 保存您的搜索历史</li>
                        <li>⭐ 收藏优质创作者</li>
                        <li>📈 跟踪营销数据</li>
                    </ul>
                    
                    <div style="text-align: center;">
                        <a href="https://beeemedia.com/creators" class="button">开始探索 →</a>
                    </div>
                    
                    <h3>💡 专业提示:</h3>
                    <p>使用具体的关键词搜索创作者，例如"美食"、"旅行"、"科技"等，能获得更精准的结果。</p>
                    
                    <p>如果您有任何问题，请随时联系我们的支持团队。</p>
                    
                    <p>祝您使用愉快！<br>
                    Beee Media 团队</p>
                </div>
                <div class="footer">
                    <p>© 2024 Beee Media. All rights reserved.<br>
                    <a href="https://beeemedia.com">beeemedia.com</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        欢迎加入 Beee Media, {user_name}!
        
        感谢您加入我们的AI驱动营销平台！
        
        您现在可以:
        - 搜索和分析TikTok创作者
        - 获取实时趋势数据  
        - 保存您的搜索历史
        - 收藏优质创作者
        - 跟踪营销数据
        
        立即开始: https://beeemedia.com/creators
        
        如有问题，请联系我们的支持团队。
        
        Beee Media 团队
        """
        
        return await self.send_email(user_email, subject, html_content, text_content)
    
    async def send_verification_email(self, user_email: str, user_name: str, 
                                    verification_link: str) -> Dict[str, Any]:
        """发送邮箱验证邮件"""
        subject = "请验证您的 Beee Media 账户邮箱"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>验证您的邮箱</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #FFA500); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .button {{ display: inline-block; background: #FFD700; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 6px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 验证您的邮箱</h1>
                </div>
                <div class="content">
                    <h2>你好, {user_name}!</h2>
                    <p>感谢您注册 Beee Media 账户！为了确保账户安全，请验证您的邮箱地址。</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_link}" class="button">验证邮箱地址 ✓</a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ 重要提醒:</strong><br>
                        • 此验证链接将在24小时后过期<br>
                        • 如果按钮无法点击，请复制以下链接到浏览器:<br>
                        <code>{verification_link}</code>
                    </div>
                    
                    <p>如果您没有注册 Beee Media 账户，请忽略此邮件。</p>
                    
                    <p>谢谢！<br>
                    Beee Media 团队</p>
                </div>
                <div class="footer">
                    <p>© 2024 Beee Media. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        验证您的 Beee Media 邮箱
        
        你好, {user_name}!
        
        请点击以下链接验证您的邮箱地址:
        {verification_link}
        
        此链接将在24小时后过期。
        
        如果您没有注册此账户，请忽略此邮件。
        
        Beee Media 团队
        """
        
        return await self.send_email(user_email, subject, html_content, text_content)
    
    async def send_password_reset_email(self, user_email: str, user_name: str,
                                      reset_link: str) -> Dict[str, Any]:
        """发送密码重置邮件"""
        subject = "重置您的 Beee Media 密码"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>重置密码</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #FFA500); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .button {{ display: inline-block; background: #FFD700; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 6px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔑 重置密码</h1>
                </div>
                <div class="content">
                    <h2>你好, {user_name}!</h2>
                    <p>我们收到了重置您的 Beee Media 账户密码的请求。</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="button">重置密码 🔄</a>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ 重要提醒:</strong><br>
                        • 此重置链接将在1小时后过期<br>
                        • 如果按钮无法点击，请复制以下链接到浏览器:<br>
                        <code>{reset_link}</code>
                    </div>
                    
                    <p>如果您没有请求重置密码，请忽略此邮件。您的密码将保持不变。</p>
                    
                    <p>为了确保账户安全，请不要将此邮件转发给他人。</p>
                    
                    <p>谢谢！<br>
                    Beee Media 团队</p>
                </div>
                <div class="footer">
                    <p>© 2024 Beee Media. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        重置您的 Beee Media 密码
        
        你好, {user_name}!
        
        请点击以下链接重置您的密码:
        {reset_link}
        
        此链接将在1小时后过期。
        
        如果您没有请求重置密码，请忽略此邮件。
        
        Beee Media 团队
        """
        
        return await self.send_email(user_email, subject, html_content, text_content)
    
    async def send_search_report_email(self, user_email: str, user_name: str,
                                     search_results: List[Dict]) -> Dict[str, Any]:
        """发送搜索报告邮件"""
        subject = f"您的 Beee Media 搜索报告 - {len(search_results)} 个结果"
        
        # 构建结果HTML
        results_html = ""
        for i, creator in enumerate(search_results[:10], 1):  # 最多显示10个结果
            results_html += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 6px;">
                <h4>{i}. {creator.get('nickname', 'Unknown Creator')}</h4>
                <p><strong>粉丝数:</strong> {creator.get('follower_count', 0):,}</p>
                <p><strong>视频数:</strong> {creator.get('total_video_count', 0):,}</p>
                <p><strong>总点赞:</strong> {creator.get('total_likes_count', 0):,}</p>
                <p><strong>简介:</strong> {creator.get('tiktok_account_bio_description', 'N/A')[:100]}...</p>
                <a href="{creator.get('tiktok_account_url', '#')}" style="color: #FFD700;">查看TikTok主页 →</a>
            </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>搜索报告</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #FFD700, #FFA500); padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 您的搜索报告</h1>
                </div>
                <div class="content">
                    <h2>你好, {user_name}!</h2>
                    <p>以下是您在 Beee Media 的搜索结果报告，共找到 <strong>{len(search_results)}</strong> 个创作者。</p>
                    
                    <h3>🎯 顶级创作者推荐:</h3>
                    {results_html}
                    
                    {"<p><em>报告中仅显示前10个结果。查看完整列表请访问我们的平台。</em></p>" if len(search_results) > 10 else ""}
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="https://beeemedia.com/creators" style="display: inline-block; background: #FFD700; color: #333; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">查看更多搜索结果 →</a>
                    </div>
                    
                    <p>感谢您使用 Beee Media！</p>
                    
                    <p>Beee Media 团队</p>
                </div>
                <div class="footer">
                    <p>© 2024 Beee Media. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(user_email, subject, html_content)

# 创建全局实例  
email_client = SendGridClient()
