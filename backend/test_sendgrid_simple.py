#!/usr/bin/env python3
"""
简化的SendGrid测试脚本
"""

import os
import sys
import ssl
import urllib3
from datetime import datetime

# 禁用SSL警告（仅用于测试）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv('../.env')

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def test_sendgrid_simple():
    """简单的SendGrid测试"""
    print("📧 开始简单SendGrid测试...")
    
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@beeemedia.com')
    from_name = os.getenv('SENDGRID_FROM_NAME', 'Beee Media')
    
    if not api_key:
        print("❌ SENDGRID_API_KEY 未设置")
        return False
    
    try:
        # 创建SendGrid客户端
        client = SendGridAPIClient(api_key=api_key)
        
        # 创建邮件
        from_email_obj = Email(from_email, from_name)
        to_email_obj = To('test@example.com')
        subject = 'SendGrid集成测试 - Beee Media'
        
        html_content = f'''
        <h1>🎉 SendGrid集成成功！</h1>
        <p>这是一封来自Beee Media的测试邮件，用于验证SendGrid API集成是否正常工作。</p>
        <p><strong>发送时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>发送邮箱:</strong> {from_email}</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
        如果您收到这封邮件，说明SendGrid API集成成功！
        </p>
        '''
        
        content = Content("text/html", html_content)
        mail = Mail(from_email_obj, to_email_obj, subject, content)
        
        # 发送邮件
        print(f"📤 正在发送邮件到 test@example.com...")
        response = client.send(mail)
        
        print(f"✅ 邮件发送成功！")
        print(f"状态码: {response.status_code}")
        print(f"消息ID: {response.headers.get('X-Message-Id', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    success = test_sendgrid_simple()
    
    if success:
        print("\n🎉 SendGrid集成测试成功！")
        print("现在可以在SendGrid控制台点击 'Verify Integration' 了。")
    else:
        print("\n❌ SendGrid集成测试失败！")
        print("请检查API密钥和网络连接。")
