import json
import os
import requests
from config.config import BASE_URL, get_headers

class BaseAPITest:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = get_headers()
        # 获取项目根目录
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def load_json_file(filename):
        """加载JSON文件"""
        # 使用项目根目录作为基准
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'json', filename)
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_response_json(response, filename):
        """保存响应到JSON文件"""
        # 使用项目根目录作为基准
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'json', 'responses', filename)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2, ensure_ascii=False)

    @staticmethod
    def verify_response_format(response):
        """验证响应格式是否符合标准"""
        response_json = response.json()
        required_fields = ['errorCode', 'errorMessage', 'httpStatus', 'data', 'success']
        
        # 验证所有必需字段都存在
        for field in required_fields:
            assert field in response_json, f"Response missing required field: {field}"
        
        # 验证httpStatus与响应状态码一致
        assert response_json['httpStatus'] == response.status_code, \
            f"Response httpStatus ({response_json['httpStatus']}) doesn't match status code ({response.status_code})"
        
        # 验证success字段与httpStatus一致
        assert response_json['success'] == (response.status_code == 200), \
            f"Response success field ({response_json['success']}) doesn't match httpStatus ({response_json['httpStatus']})"
        
        return response_json

    def compare_response_data(self, response, expected_file):
        """比较响应数据与预期结果"""
        response_json = self.verify_response_format(response)
        expected = self.load_json_file(expected_file)
        actual = response_json['data']
        return expected == actual

    def make_request(self, method, endpoint, data=None, expected_status=200):
        """发送HTTP请求并验证响应"""
        url = f"{self.base_url}{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        
        # 验证响应状态码
        assert response.status_code == expected_status, \
            f"Expected status code {expected_status}, but got {response.status_code}"
        
        # 验证响应格式
        self.verify_response_format(response)
        
        return response 