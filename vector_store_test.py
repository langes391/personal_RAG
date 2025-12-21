from vector_store import VectorStore

class TestVectorStore:
    def setup_method(self):
        """在每个测试方法前设置"""
        # 使用mock embedding初始化向量存储
        self.vector_store = VectorStore(use_mock=True)
    
    def add_texts_test(self):
        """测试添加文本到向量存储"""
        # 准备测试文本
        texts = [
            "这是第一段测试文本",
            "这是第二段测试文本",
            "这是第三段测试文本"
        ]
        
        # 添加文本到向量存储
        self.vector_store.add_texts(texts)
        
        # 验证向量存储已初始化
        assert self.vector_store.vector_store is not None
    
    def similarity_search_test(self):
        """测试相似性搜索功能"""
        # 准备测试文本
        texts = [
            "这是关于Python的测试文本",
            "这是关于Java的测试文本",
            "这是关于C++的测试文本",
            "这是关于JavaScript的测试文本"
        ]
        
        # 添加文本到向量存储
        self.vector_store.add_texts(texts)
        
        # 测试相似性搜索
        query = "Python语言"
        results = self.vector_store.similarity_search(query, k=2)
        
        # 验证搜索结果
        assert len(results) == 2
        assert all(isinstance(result, str) for result in results)
    
    def similarity_search_empty_store_test(self):
        """测试在空向量存储中搜索"""
        # 直接测试搜索，不添加任何文本
        query = "测试查询"
        results = self.vector_store.similarity_search(query)
        
        # 验证结果为空列表
        assert results == []
    
    def reset_test(self):
        """测试重置向量存储"""
        # 准备测试文本
        texts = ["测试文本1", "测试文本2"]
        
        # 添加文本到向量存储
        self.vector_store.add_texts(texts)
        
        # 重置向量存储
        self.vector_store.reset()
        
        # 验证向量存储已重置
        assert self.vector_store.vector_store is None
        
        # 测试重置后搜索结果为空
        query = "测试查询"
        results = self.vector_store.similarity_search(query)
        assert results == []