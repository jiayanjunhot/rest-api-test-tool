import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
BASE_URL = os.getenv('API_BASE_URL', 'http://api.example.com')
API_TOKEN = os.getenv('API_TOKEN', '')

# 请求头
def get_headers():
    return {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    } 