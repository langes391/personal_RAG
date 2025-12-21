# 个人知识库问答系统

一个基于Streamlit的个人知识库问答系统，支持上传文档并进行智能问答，集成了多种LLM模型和向量存储方案。

## 🌟 核心功能

- ✅ 支持上传多种类型文档（PDF、TXT、DOCX）
- ✅ 智能文本分块和向量存储
- ✅ 基于上下文的精准问答
- ✅ 实时聊天交互界面
- ✅ 支持清除所有数据重置系统
- ✅ 集成多种LLM模型（OpenAI、DeepSeek）
- ✅ 支持Mock Embedding用于测试和离线使用
- ✅ 向量存储持久化，支持页面刷新后数据保留

## 🛠 技术栈

- **前端框架**：Streamlit
- **文档解析**：PyPDF2、python-docx
- **文本处理**：LangChain
- **向量存储**：自定义In-Memory Vector Store + ChromaDB
- **LLM集成**：OpenAI API、DeepSeek API
- **测试框架**：Pytest

## 🚀 快速开始

### 1. 环境要求

- Python 3.10+ 
- pip 21.0+

### 2. 安装步骤

#### 2.1 克隆项目
```bash
git clone https://github.com/your_username/personal_RAG.git
cd personal_RAG
```

#### 2.2 创建虚拟环境（推荐）
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 2.3 安装依赖
```bash
pip install -r requirements.txt
```

#### 2.4 配置API密钥

创建`.env`文件，根据需要添加API密钥：
```
# OpenAI API配置（可选）
OPENAI_API_KEY=your_openai_api_key_here

# DeepSeek API配置（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**注意**：至少需要配置其中一个API密钥，或使用Mock模式运行。

### 3. 启动应用

```bash
streamlit run app.py
```

应用将在浏览器中自动打开，默认地址：http://localhost:8503

## 📖 使用指南

1. **上传文档**：在左侧上传区选择要上传的文档（PDF、TXT、DOCX）
2. **等待处理**：系统会自动解析文档并生成向量存储
3. **提问**：在右侧聊天窗口输入问题，获取智能回答
4. **清除数据**：点击"清除所有数据"按钮可重置系统

## 📁 项目结构

```
├── app.py                  # Streamlit应用入口
├── config.py               # 配置文件
├── document_processor.py   # 文件解析和文本分块模块
├── vector_store.py         # 向量存储和检索模块
├── llm_integration.py      # LLM调用模块
├── requirements.txt        # 依赖清单
├── document_processor_test.py   # 文档处理测试
├── vector_store_test.py         # 向量存储测试
├── llm_integration_test.py      # LLM集成测试
├── test_persistence.py          # 持久化功能测试
├── full_flow_test.py            # 完整流程测试
├── test_file_upload_fix.py      # 文件上传修复测试
└── README.md               # 项目说明
```

## 🔧 配置说明

可以在`config.py`文件中调整以下配置：

### 文档处理
- `CHUNK_SIZE`：文本分块大小（默认：1000）
- `CHUNK_OVERLAP`：分块重叠大小（默认：200）

### 向量存储
- `VECTOR_STORE_PATH`：向量存储路径（默认："./vector_store"）
- `UPLOAD_DIR`：文件上传目录（默认："./uploads"）

### LLM配置
- `LLM_MODEL`：默认语言模型（默认："gpt-3.5-turbo"）
- `TEMPERATURE`：生成温度（默认：0.7）
- `MAX_TOKENS`：最大生成tokens（默认：500）
- `MAX_RETRIES`：API重试次数（默认：2）

### DeepSeek API配置
- `DEEPSEEK_BASE_URL`：DeepSeek API地址
- `DEEPSEEK_MODEL`：DeepSeek模型名称

## 🧪 测试

### 运行单元测试
```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest document_processor_test.py vector_store_test.py llm_integration_test.py -v
```

### 运行完整流程测试
```bash
python full_flow_test.py
```

## 📋 注意事项

1. **API密钥安全**：不要将API密钥提交到GitHub，使用`.env`文件管理
2. **文档大小限制**：建议单个文件不超过10MB
3. **模型选择**：根据需要在`config.py`中切换不同的LLM模型
4. **离线使用**：可通过设置`use_mock=True`在离线环境下测试
5. **数据持久化**：向量存储会自动保存，页面刷新后数据不会丢失

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，欢迎提交Issue或联系项目维护者。

---

**个人知识库问答系统** - 让知识触手可及！