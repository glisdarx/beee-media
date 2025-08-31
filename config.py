# -*- coding: utf-8 -*-
"""
TikTok自动化配置文件
基于MD文件中的API端点信息
"""

# TikHub API配置
TIKHUB_API_KEY = "w7MRRTtG50I0nQQRwUXvkCUdwyZXk5mI4alf2QvjknZZ4XIzYNAv/kK8AA=="
TIKHUB_BASE_URL = "https://api.tikhub.io"

# API端点配置 (基于MD文件中的OpenAPI规范)
API_ENDPOINTS = {
    # 搜索端点
    "comprehensive_search": "/api/v1/tiktok/app/v3/fetch_general_search_result",  # 综合搜索
    "general_search": "/api/v1/tiktok/web/fetch_general_search",  # Web通用搜索
    
    # 用户信息端点
    "user_profile_app": "/api/v1/tiktok/app/v3/handler_user_profile",  # App V3用户信息
    "user_profile_web": "/api/v1/tiktok/web/fetch_user_profile",  # Web用户信息
    
    # 创作者信息端点
    "creator_info": "/api/v1/tiktok/app/v3/fetch_creator_info",  # 创作者信息
}

# 搜索配置
DEFAULT_KEYWORDS = [
    "ChatGPT",
    "AI", 
    "人工智能",
    "机器学习",
    "编程",
    "科技"
]

# 用户收集配置
MAX_USERS_PER_KEYWORD = 50
REQUEST_DELAY = 1  # 请求间隔（秒）

# 输出配置
OUTPUT_FORMATS = ["csv", "json", "excel"]
OUTPUT_DIR = "output"

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# 请求配置
MAX_RETRIES = 3  # 最大重试次数
RETRY_DELAY = 2  # 重试间隔(秒)