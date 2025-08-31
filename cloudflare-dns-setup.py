#!/usr/bin/env python3
import requests
import json
import sys

# Cloudflare API配置
API_TOKEN = "ohZJC7hCB-7u60R8UcK44B_l36U2qzl7Lus727zH"
ZONE_NAME = "beeemedia.com"
PROJECT_NAME = "beee-media"

# API Headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_zone_id():
    """获取域名Zone ID"""
    url = "https://api.cloudflare.com/client/v4/zones"
    params = {"name": ZONE_NAME}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"] and data["result"]:
            zone_id = data["result"][0]["id"]
            print(f"✅ 找到域名Zone ID: {zone_id}")
            return zone_id
        else:
            print(f"❌ 未找到域名: {ZONE_NAME}")
            return None
    
    print(f"❌ 获取Zone ID失败: {response.text}")
    return None

def get_existing_dns_records(zone_id):
    """获取现有DNS记录"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            records = data["result"]
            print(f"📋 现有DNS记录数量: {len(records)}")
            
            for record in records:
                print(f"   - {record['type']} {record['name']} -> {record['content']}")
            
            return records
    
    print(f"❌ 获取DNS记录失败: {response.text}")
    return []

def create_cname_record(zone_id, subdomain, target):
    """创建CNAME记录"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    
    record_data = {
        "type": "CNAME",
        "name": subdomain,
        "content": target,
        "ttl": 1  # 自动TTL
    }
    
    response = requests.post(url, headers=headers, json=record_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            record = data["result"]
            print(f"✅ CNAME记录创建成功: {record['name']} -> {record['content']}")
            return True
        else:
            print(f"❌ 创建CNAME记录失败: {data}")
            return False
    
    print(f"❌ API请求失败: {response.text}")
    return False

def main():
    print("🚀 开始配置Cloudflare DNS记录")
    print("=" * 50)
    
    # 1. 获取Zone ID
    zone_id = get_zone_id()
    if not zone_id:
        sys.exit(1)
    
    # 2. 查看现有DNS记录
    print(f"\n📋 检查现有DNS记录...")
    existing_records = get_existing_dns_records(zone_id)
    
    # 检查是否已经有指向Pages的记录
    pages_target = f"{PROJECT_NAME}.pages.dev"
    has_root_record = False
    has_www_record = False
    
    for record in existing_records:
        if record["name"] == ZONE_NAME and record["content"] == pages_target:
            has_root_record = True
            print(f"ℹ️  根域名记录已存在: {ZONE_NAME} -> {pages_target}")
        
        if record["name"] == f"www.{ZONE_NAME}" and record["content"] == pages_target:
            has_www_record = True
            print(f"ℹ️  www记录已存在: www.{ZONE_NAME} -> {pages_target}")
    
    # 3. 创建缺失的记录
    success = True
    
    if not has_root_record:
        print(f"\n🔧 创建根域名CNAME记录...")
        if not create_cname_record(zone_id, ZONE_NAME, pages_target):
            success = False
    
    if not has_www_record:
        print(f"\n🔧 创建www子域名CNAME记录...")
        if not create_cname_record(zone_id, f"www.{ZONE_NAME}", pages_target):
            success = False
    
    if success:
        print(f"\n🎉 DNS配置完成！")
        print(f"🌐 您的域名将在几分钟内生效:")
        print(f"   - https://{ZONE_NAME}")
        print(f"   - https://www.{ZONE_NAME}")
        print(f"\n⏰ 请等待2-10分钟让DNS全球传播完成")
        
        print(f"\n📊 验证命令:")
        print(f"   curl -I https://{ZONE_NAME}")
        print(f"   nslookup {ZONE_NAME}")
        
    else:
        print(f"\n❌ DNS配置过程中出现错误")
        print(f"💡 建议：登录Cloudflare控制台手动添加DNS记录")
        print(f"   类型: CNAME")
        print(f"   名称: {ZONE_NAME}")
        print(f"   目标: {pages_target}")

if __name__ == "__main__":
    main()
