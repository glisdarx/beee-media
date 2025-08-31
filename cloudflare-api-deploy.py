#!/usr/bin/env python3
import requests
import json
import sys
import time

# Cloudflare API配置
API_TOKEN = "ohZJC7hCB-7u60R8UcK44B_l36U2qzl7Lus727zH"
ACCOUNT_EMAIL = "your-email@example.com"  # 需要您提供
ZONE_NAME = "beeemedia.com"
PROJECT_NAME = "beee-media"
GITHUB_REPO = "glisdarx/beee-media"

# API Headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_account_id():
    """获取账户ID"""
    url = "https://api.cloudflare.com/client/v4/accounts"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"] and data["result"]:
            account_id = data["result"][0]["id"]
            print(f"✅ 获取账户ID成功: {account_id}")
            return account_id
    
    print(f"❌ 获取账户ID失败: {response.text}")
    return None

def get_zone_id():
    """获取域名Zone ID"""
    url = f"https://api.cloudflare.com/client/v4/zones?name={ZONE_NAME}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"] and data["result"]:
            zone_id = data["result"][0]["id"]
            print(f"✅ 获取域名Zone ID成功: {zone_id}")
            return zone_id
    
    print(f"❌ 获取域名Zone ID失败: {response.text}")
    return None

def create_pages_project(account_id):
    """创建Cloudflare Pages项目"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    
    project_data = {
        "name": PROJECT_NAME,
        "production_branch": "main",
        "source": {
            "type": "github",
            "config": {
                "owner": "glisdarx",
                "repo_name": "beee-media",
                "production_branch": "main",
                "pr_comments_enabled": True,
                "deployments_enabled": True,
                "production_deployments_enabled": True
            }
        },
        "build_config": {
            "build_command": "echo 'Static deployment ready'",
            "destination_dir": "/",
            "root_dir": "/",
            "web_analytics_tag": None,
            "web_analytics_token": None
        },
        "deployment_configs": {
            "production": {
                "env_vars": {
                    "TIKHUB_API_KEY": {
                        "value": "w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA=="
                    }
                }
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=project_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            project = data["result"]
            print(f"✅ Pages项目创建成功: {project['name']}")
            print(f"🌐 项目URL: {project['subdomain']}")
            return project
    
    print(f"❌ 创建Pages项目失败: {response.text}")
    return None

def add_custom_domain(account_id, project_name, domain):
    """添加自定义域名"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/domains"
    
    domain_data = {
        "name": domain
    }
    
    response = requests.post(url, headers=headers, json=domain_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print(f"✅ 自定义域名添加成功: {domain}")
            return True
    
    print(f"❌ 添加自定义域名失败: {response.text}")
    return False

def main():
    print("🚀 开始使用Cloudflare API自动部署 Beee Media")
    print("=" * 50)
    
    # 1. 获取账户ID
    account_id = get_account_id()
    if not account_id:
        sys.exit(1)
    
    # 2. 获取Zone ID
    zone_id = get_zone_id()
    if not zone_id:
        print("⚠️  警告: 无法获取域名Zone ID，但可以继续部署")
    
    # 3. 创建Pages项目
    project = create_pages_project(account_id)
    if not project:
        sys.exit(1)
    
    # 4. 添加自定义域名
    print("\n🌐 添加自定义域名...")
    time.sleep(2)  # 等待项目完全创建
    
    success = add_custom_domain(account_id, PROJECT_NAME, ZONE_NAME)
    if success:
        print(f"✅ 域名配置成功: https://{ZONE_NAME}")
    
    print("\n🎉 部署完成！")
    print(f"🌟 您的网站将在几分钟内可以通过以下地址访问:")
    print(f"   - https://{ZONE_NAME}")
    print(f"   - https://{ZONE_NAME}/creators")
    
    print(f"\n📊 项目管理:")
    print(f"   - Cloudflare Pages: https://dash.cloudflare.com/{account_id}/pages/view/{PROJECT_NAME}")
    print(f"   - GitHub仓库: https://github.com/{GITHUB_REPO}")

if __name__ == "__main__":
    main()
