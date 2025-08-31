#!/usr/bin/env python3
"""
测试SendGrid邮件发送功能
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

from services.sendgrid_client import SendGridClient

async def test_sendgrid():
    """测试SendGrid邮件发送"""
    print("📧 开始测试SendGrid集成...")
    
    # 创建SendGrid客户端
    email_client = SendGridClient()
    
    # 发送测试邮件
    result = await email_client.send_email(
        to_email='test@example.com',
        subject='SendGrid集成测试 - Beee Media',
        html_content=f'''
        <h1>🎉 SendGrid集成成功！</h1>
        <p>这是一封来自Beee Media的测试邮件，用于验证SendGrid API集成是否正常工作。</p>
        <p><strong>发送时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>发送邮箱:</strong> {email_client.from_email}</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
        如果您收到这封邮件，说明SendGrid API集成成功！
        </p>
        ''',
        text_content=f'SendGrid集成测试成功！这是一封来自Beee Media的测试邮件。发送时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )
    
    print("\n📧 测试邮件发送结果:")
    print(f"成功: {result.get('success', False)}")
    print(f"消息: {result.get('message', '未知')}")
    if result.get('error'):
        print(f"错误: {result.get('error')}")
    
    return result

if __name__ == "__main__":
    # 运行测试
    result = asyncio.run(test_sendgrid())
    
    if result.get('success'):
        print("\n✅ SendGrid集成测试成功！")
        print("现在可以在SendGrid控制台点击 'Verify Integration' 了。")
    else:
        print("\n❌ SendGrid集成测试失败！")
        print("请检查API密钥和配置。")
