import json
import os
import unittest

import requests
from config.config import BASE_URL, get_headers


class BaseAPITest(unittest.TestCase):
    def setUp(self):
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
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'json', 'responses',
                                 filename)
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
        actual = response_json['data']

        # 检查expected_file是否存在
        expected_path = os.path.join(self.project_root, 'json', expected_file)
        if not os.path.exists(expected_path):
            # 如果expected_file不存在，则actual应该为空
            assert actual is None or actual == {}, \
                f"Expected file {expected_file} not found, but response data is not empty: {actual}"
            return True

        # 如果expected_file存在，则比较数据
        expected = self.load_json_file(expected_file)
        return expected == actual

    def prepare_form_data(self, test_case):
        """准备form-data请求数据"""
        if not test_case.get('is_form_data'):
            return None

        # 加载请求参数
        request_data = self.load_json_file(test_case['request_file'])
        params = request_data.get('params', {})

        # 准备文件
        file_path = os.path.join(self.project_root, test_case['file_path'])
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # 创建multipart/form-data
        files = {
            'file': (
                params.get('fileName', os.path.basename(file_path)),
                open(file_path, 'rb'),
                params.get('fileType', 'application/octet-stream')
            )
        }

        # 添加其他参数
        data = {
            'description': params.get('description', ''),
            'category': params.get('category', ''),
            'fileName': params.get('fileName', ''),
            'fileType': params.get('fileType', '')
        }

        return {'files': files, 'data': data}

    def make_request(self, method, endpoint, data=None, is_form_data=False):
        """发送HTTP请求并验证响应"""
        url = f"{self.base_url}{endpoint}"

        if is_form_data:
            # 处理form-data请求
            form_data = self.prepare_form_data(data)
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                files=form_data['files'],
                data=form_data['data'],
                verify=False
            )
        else:
            # 处理普通JSON请求
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                verify=False
            )

        return response
