# REST API 测试项目

这是一个使用Python 3.11开发的REST API测试项目。

## 项目结构

```
.
├── config/             # 配置文件目录
│   └── config.py      # 配置类
├── json/              # JSON文件目录
│   ├── requests/      # 请求数据
│   ├── responses/     # 响应数据
│   └── expected/      # 预期结果
├── tests/             # 测试文件目录
│   ├── base_test.py   # 测试基类
│   └── test_*.py      # 具体测试用例
├── .env               # 环境变量配置
├── requirements.txt   # 项目依赖
└── README.md         # 项目说明
```

## 安装

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
- 复制 `.env.example` 为 `.env`
- 修改 `.env` 中的配置项

## 运行测试

```bash
pytest tests/
```

## 添加新的API测试

1. 在 `json/requests/` 目录下创建请求数据JSON文件
2. 在 `json/expected/` 目录下创建预期响应JSON文件
3. 在 `tests/` 目录下创建新的测试文件，继承 `BaseAPITest` 类
4. 编写测试用例

## 注意事项

- 所有API请求都需要通过Authorization header进行鉴权
- 响应状态码200表示成功
- 响应结果会与预期JSON文件进行对比 