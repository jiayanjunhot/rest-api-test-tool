import json
import os

from tests.base_test import BaseAPITest


class TestUserAPI(BaseAPITest):
    def setUp(self):
        super().setUp()
        # 加载测试配置
        config_path = os.path.join(self.project_root, 'config', 'api_test_config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            self.test_config = json.load(f)

    def run_test_case(self, test_case):
        """运行单个测试用例"""
        # 准备请求数据
        request_data = None
        if test_case['request_file']:
            request_data = self.load_json_file(test_case['request_file'])

        # 发送请求
        response = self.make_request(
            method=test_case['method'],
            endpoint=test_case['endpoint'],
            data=test_case if test_case.get('is_form_data') else request_data,
            is_form_data=test_case.get('is_form_data', False)
        )

        # 保存响应
        self.save_response_json(response, test_case['response_file'])

        # 比较响应数据
        assert self.compare_response_data(response, test_case['expected_file'])

    def test_all_cases(self):
        """运行所有测试用例"""
        for test_case in self.test_config['test_cases']:
            self.run_test_case(test_case)

    # 为每个测试用例创建单独的测试方法
    def test_get_user_info(self):
        """测试获取用户信息"""
        test_case = next(tc for tc in self.test_config['test_cases'] if tc['name'] == 'get_user_info')
        self.run_test_case(test_case)

    def test_create_user(self):
        """测试创建用户"""
        test_case = next(tc for tc in self.test_config['test_cases'] if tc['name'] == 'create_user')
        self.run_test_case(test_case)

    def test_upload_file(self):
        """测试文件上传"""
        test_case = next(tc for tc in self.test_config['test_cases'] if tc['name'] == 'upload_file')
        self.run_test_case(test_case)
