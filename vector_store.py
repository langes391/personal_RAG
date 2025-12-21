from langchain_community.embeddings import OpenAIEmbeddings
from langchain.embeddings.base import Embeddings
import numpy as np
import os
import pickle
from dotenv import load_dotenv
from config import EMBEDDING_MODEL, VECTOR_STORE_PATH, EMBEDDING_BASE_URL

# 加载.env文件
load_dotenv()

# 确保向量存储目录存在
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

class MockEmbeddings(Embeddings):
    """用于测试的Mock Embeddings类"""
    def __init__(self, embedding_dim=1536):
        self.embedding_dim = embedding_dim
    
    def embed_documents(self, texts):
        """返回随机向量作为文档嵌入"""
        return [np.random.rand(self.embedding_dim).tolist() for _ in texts]
    
    def embed_query(self, text):
        """返回随机向量作为查询嵌入"""
        return np.random.rand(self.embedding_dim).tolist()

class VectorStore:
    def __init__(self, use_mock=False):
        """初始化向量存储"""
        if use_mock:
            self.embeddings = MockEmbeddings()
        else:
            # 从环境变量获取API密钥
            openai_api_key = os.getenv("OPENAI_API_KEY")
            self.embeddings = OpenAIEmbeddings(
                model=EMBEDDING_MODEL,
                api_key=openai_api_key,
                base_url=EMBEDDING_BASE_URL
            )
        
        # 使用内存存储，支持持久化
        self.texts = []
        self.embeddings_list = []
        
        # 尝试加载已保存的向量存储
        self._load_vector_store()
    
    def _cosine_similarity(self, a, b):
        """计算余弦相似度"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def add_texts(self, texts):
        """将文本块添加到向量存储"""
        try:
            # 嵌入文本
            embeddings = self.embeddings.embed_documents(texts)
            
            # 存储文本和嵌入
            self.texts.extend(texts)
            self.embeddings_list.extend(embeddings)
            
            # 保存向量存储到磁盘
            self._save_vector_store()
        except Exception as e:
            print(f"DeepSeek API调用失败: {str(e)}")
            print("自动切换到MockEmbeddings...")
            
            # 切换到MockEmbeddings作为回退
            self.embeddings = MockEmbeddings()
            
            # 使用MockEmbeddings嵌入文本
            embeddings = self.embeddings.embed_documents(texts)
            
            # 存储文本和嵌入
            self.texts.extend(texts)
            self.embeddings_list.extend(embeddings)
            
            # 保存向量存储到磁盘
            self._save_vector_store()
    
    def similarity_search(self, query, k=4):
        """根据查询检索最相似的文本块"""
        if not self.texts:
            return []
        
        try:
            # 嵌入查询
            query_embedding = self.embeddings.embed_query(query)
            
            # 计算相似度
            similarities = [
                (text, self._cosine_similarity(query_embedding, emb))
                for text, emb in zip(self.texts, self.embeddings_list)
            ]
            
            # 按相似度排序
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # 返回前k个结果
            return [text for text, _ in similarities[:k]]
        except Exception as e:
            print(f"DeepSeek API调用失败: {str(e)}")
            print("自动切换到MockEmbeddings...")
            
            # 切换到MockEmbeddings作为回退
            self.embeddings = MockEmbeddings()
            
            try:
                # 使用MockEmbeddings嵌入查询
                query_embedding = self.embeddings.embed_query(query)
                
                # 计算相似度
                similarities = [
                    (text, self._cosine_similarity(query_embedding, emb))
                    for text, emb in zip(self.texts, self.embeddings_list)
                ]
                
                # 按相似度排序
                similarities.sort(key=lambda x: x[1], reverse=True)
                
                # 返回前k个结果
                return [text for text, _ in similarities[:k]]
            except Exception as e2:
                # 如果仍然失败，返回默认结果
                print(f"MockEmbeddings也失败了: {str(e2)}")
                # 返回前k个文本块作为默认结果
                return self.texts[:min(k, len(self.texts))]
    
    def reset(self):
        """重置向量存储"""
        self.texts = []
        self.embeddings_list = []
        
        # 删除保存的向量存储文件
        self._delete_vector_store()
    
    def _save_vector_store(self):
        """将向量存储保存到磁盘"""
        try:
            # 保存嵌入模型类型和向量数据
            data = {
                "texts": self.texts,
                "embeddings_list": self.embeddings_list,
                "embeddings_type": "mock" if isinstance(self.embeddings, MockEmbeddings) else "real"
            }
            file_path = os.path.join(VECTOR_STORE_PATH, "vector_store.pkl")
            with open(file_path, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            raise Exception(f"保存向量存储失败: {str(e)}")
    
    def _load_vector_store(self):
        """从磁盘加载向量存储"""
        try:
            file_path = os.path.join(VECTOR_STORE_PATH, "vector_store.pkl")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    data = pickle.load(f)
                    self.texts = data["texts"]
                    self.embeddings_list = data["embeddings_list"]
                    
                    # 检查保存的嵌入模型类型
                    embeddings_type = data.get("embeddings_type", "real")
                    
                    # 如果保存的是mock类型，但当前是real类型，切换到mock
                    if embeddings_type == "mock" and not isinstance(self.embeddings, MockEmbeddings):
                        print(f"检测到向量存储使用的是MockEmbeddings，自动切换...")
                        self.embeddings = MockEmbeddings()
        except Exception as e:
            print(f"加载向量存储失败: {str(e)}")
            # 加载失败时使用空存储
            self.texts = []
            self.embeddings_list = []
    
    def _delete_vector_store(self):
        """删除磁盘上的向量存储文件"""
        try:
            file_path = os.path.join(VECTOR_STORE_PATH, "vector_store.pkl")
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"删除向量存储失败: {str(e)}")