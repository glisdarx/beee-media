#!/usr/bin/env python3
import requests
import json
import sys
import time

# Cloudflare API配置
API_TOKEN = "ohZJC7hCB-7u60R8UcK44B_l36U2qzl7Lus727zH"
ACCOUNT_ID = "f107fe1129d0a81088698148e5c9bca2"
ZONE_NAME = "beeemedia.com"
PROJECT_NAME = "beee-media"

# API Headers
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def list_pages_projects():
    """列出所有Pages项目"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            projects = data["result"]
            print(f"📋 找到 {len(projects)} 个Pages项目:")
            for project in projects:
                print(f"   - {project['name']} ({project['subdomain']})")
            return projects
    
    print(f"❌ 获取项目列表失败: {response.text}")
    return []

def get_project_details(project_name):
    """获取项目详情"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{project_name}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            project = data["result"]
            print(f"✅ 项目详情获取成功: {project['name']}")
            print(f"   📁 状态: {project.get('production_deployment', {}).get('deployment_trigger', {}).get('type', 'unknown')}")
            print(f"   🌐 默认域名: {project['subdomain']}")
            
            # 显示现有的自定义域名
            domains = project.get("domains", [])
            if domains:
                print(f"   🔗 现有域名:")
                for domain in domains:
                    if isinstance(domain, dict):
                        print(f"      - {domain.get('name', 'unknown')} (状态: {domain.get('status', 'unknown')})")
                    else:
                        print(f"      - {domain}")
            else:
                print(f"   🔗 暂无自定义域名")
            
            return project
    
    print(f"❌ 获取项目详情失败: {response.text}")
    return None

def add_custom_domain(project_name, domain):
    """添加自定义域名"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{project_name}/domains"
    
    domain_data = {
        "name": domain
    }
    
    response = requests.post(url, headers=headers, json=domain_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print(f"✅ 自定义域名添加成功: {domain}")
            domain_info = data["result"]
            print(f"   📊 域名状态: {domain_info.get('status', 'unknown')}")
            print(f"   🔄 验证状态: {domain_info.get('verification_data', {}).get('status', 'unknown')}")
            return True
    
    # 检查是否是域名已存在的错误
    error_text = response.text
    if "already exists" in error_text or "already added" in error_text:
        print(f"ℹ️  域名 {domain} 已经存在，无需重复添加")
        return True
    
    print(f"❌ 添加自定义域名失败: {error_text}")
    return False

def update_project_settings(project_name):
    """更新项目设置"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{project_name}"
    
    # 获取当前设置
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ 无法获取当前项目设置")
        return False
    
    current_data = response.json()["result"]
    
    # 更新环境变量
    deployment_configs = current_data.get("deployment_configs", {})
    if "production" not in deployment_configs:
        deployment_configs["production"] = {}
    if "env_vars" not in deployment_configs["production"]:
        deployment_configs["production"]["env_vars"] = {}
    
    deployment_configs["production"]["env_vars"]["TIKHUB_API_KEY"] = {
        "value": "w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA=="
    }
    
    update_data = {
        "deployment_configs": deployment_configs
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            print(f"✅ 项目环境变量更新成功")
            return True
    
    print(f"⚠️  环境变量更新失败，但不影响部署: {response.text}")
    return False

def trigger_deployment(project_name):
    """触发重新部署"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{project_name}/deployments"
    
    deploy_data = {
        "branch": "main"
    }
    
    response = requests.post(url, headers=headers, json=deploy_data)
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            deployment = data["result"]
            print(f"✅ 重新部署触发成功")
            print(f"   🆔 部署ID: {deployment['id']}")
            print(f"   🌿 分支: {deployment.get('source', {}).get('branch', 'unknown')}")
            return True
    
    print(f"⚠️  触发重新部署失败，但项目应该会自动部署: {response.text}")
    return False

def main():
    print("🚀 开始配置现有的Cloudflare Pages项目")
    print("=" * 50)
    
    # 1. 列出现有项目
    projects = list_pages_projects()
    
    # 2. 检查目标项目是否存在
    target_project = None
    for project in projects:
        if project["name"] == PROJECT_NAME:
            target_project = project
            break
    
    if not target_project:
        print(f"❌ 未找到项目: {PROJECT_NAME}")
        print("请先通过Web界面创建Pages项目，或使用不同的项目名称")
        sys.exit(1)
    
    print(f"\n🎯 找到目标项目: {PROJECT_NAME}")
    
    # 3. 获取项目详情
    project_details = get_project_details(PROJECT_NAME)
    if not project_details:
        sys.exit(1)
    
    # 4. 添加自定义域名
    print(f"\n🌐 添加自定义域名: {ZONE_NAME}")
    domain_success = add_custom_domain(PROJECT_NAME, ZONE_NAME)
    
    # 5. 更新项目设置
    print(f"\n⚙️ 更新环境变量...")
    update_project_settings(PROJECT_NAME)
    
    # 6. 触发重新部署
    print(f"\n🔄 触发重新部署...")
    trigger_deployment(PROJECT_NAME)
    
    print(f"\n🎉 配置完成！")
    print(f"🌟 您的网站将在几分钟内可以通过以下地址访问:")
    print(f"   - https://{ZONE_NAME}")
    print(f"   - https://{ZONE_NAME}/creators")
    print(f"   - https://{target_project['subdomain']} (备用域名)")
    
    print(f"\n📊 项目管理:")
    print(f"   - Cloudflare Pages: https://dash.cloudflare.com/{ACCOUNT_ID}/pages/view/{PROJECT_NAME}")
    print(f"   - GitHub仓库: https://github.com/glisdarx/beee-media")
    
    print(f"\n⏰ 请等待2-5分钟让DNS生效，然后访问您的网站！")

if __name__ == "__main__":
    main()
