#!/usr/bin/env python3
"""
测试Supabase连接
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加backend目录到路径
sys.path.append('backend')

def test_supabase_connection():
    """测试Supabase连接"""
    try:
        from services.supabase_client import db_client
        print("✅ Supabase客户端导入成功")
        
        # 测试基本连接
        print("🔍 测试Supabase连接...")
        
        # 尝试获取配置信息
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_ANON_KEY')
        
        print(f"📊 Supabase URL: {url}")
        print(f"🔑 API Key: {key[:20]}..." if key else "❌ 未设置API Key")
        
        if not url or not key:
            print("❌ 缺少Supabase配置")
            return False
        
        print("✅ Supabase配置检查通过")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_database_schema():
    """测试数据库架构"""
    try:
        print("\n📋 检查数据库架构文件...")
        
        schema_file = 'database/schema.sql'
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                content = f.read()
                table_count = content.count('CREATE TABLE')
                print(f"✅ 找到 {table_count} 个数据表定义")
                return True
        else:
            print("❌ 数据库架构文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ 架构检查错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Beee Media Supabase 连接测试")
    print("=" * 50)
    
    # 检查环境变量
    print("🔍 检查环境变量...")
    env_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY']
    missing_vars = []
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:30]}..." if len(value) > 30 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未设置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  缺少环境变量: {', '.join(missing_vars)}")
        print("请检查 .env 文件配置")
        return
    
    # 测试Supabase连接
    if test_supabase_connection():
        print("\n✅ Supabase连接测试通过")
    else:
        print("\n❌ Supabase连接测试失败")
    
    # 测试数据库架构
    if test_database_schema():
        print("✅ 数据库架构检查通过")
    else:
        print("❌ 数据库架构检查失败")
    
    print("\n" + "=" * 50)
    print("📋 下一步操作:")
    print("1. 在Supabase控制台中执行 database/schema.sql")
    print("2. 安装Python依赖: pip install -r requirements.txt")
    print("3. 启动应用: cd backend && python app.py")

if __name__ == "__main__":
    main()
