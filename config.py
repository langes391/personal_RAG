# 配置文件

# 文档处理配置
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# 文件存储配置
UPLOAD_DIR = "./uploads"  # 上传文件保存目录

# 向量存储配置
VECTOR_STORE_PATH = "./vector_store"
EMBEDDING_MODEL = "deepseek-ai/text-embedding-v1"  # DeepSeek API支持的嵌入模型

# LLM配置
LLM_MODEL = "deepseek-chat"
BASE_URL = "https://api.deepseek.com"
EMBEDDING_BASE_URL = "https://api.deepseek.com/v1"  # 嵌入模型API地址，添加v1版本号
TEMPERATURE = 0.7
MAX_TOKENS = 500
MAX_RETRIES = 1  # 减少重试次数，默认1次重试

# Streamlit配置
APP_TITLE = "个人知识库问答系统"
APP_DESCRIPTION = "上传文档，然后提问，系统将根据文档内容回答您的问题"

# 支持的文档类型
SUPPORTED_FILE_TYPES = [".pdf", ".txt", ".docx"]