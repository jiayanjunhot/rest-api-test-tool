import os
import json
from typing import Dict, Any, Optional, Tuple

class FormDataHandler:
    def __init__(self, project_root: str):
        self.project_root = project_root

    def load_form_data_config(self, config_file: str) -> Dict[str, Any]:
        """加载form-data配置文件"""
        config_path = os.path.join(self.project_root, 'json', 'requests', config_file)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Form data config file not found: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def prepare_form_data(self, config_file: str, file_path: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """准备form-data请求数据
        
        Args:
            config_file: form-data配置文件路径
            file_path: 要上传的文件路径
            
        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: (files, data) 元组
        """
        # 加载配置
        config = self.load_form_data_config(config_file)
        params = config.get('params', {})

        # 准备文件
        full_file_path = os.path.join(self.project_root, file_path)
        if not os.path.exists(full_file_path):
            raise FileNotFoundError(f"File not found: {full_file_path}")

        # 创建multipart/form-data
        files = {
            'file': (
                params.get('fileName', os.path.basename(full_file_path)),
                open(full_file_path, 'rb'),
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

        return files, data 