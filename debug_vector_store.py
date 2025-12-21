from vector_store import VectorStore, MockEmbeddings
from langchain_community.vectorstores import Chroma
import os
import tempfile

print("=== 向量存储调试 ===")

# 1. 测试MockEmbeddings
print("\n1. 测试MockEmbeddings...")
mock_embeddings = MockEmbeddings()
try:
    # 测试embed_documents
    test_texts = ["测试文本1", "测试文本2"]
    embeddings = mock_embeddings.embed_documents(test_texts)
    print(f"   ✓ embed_documents成功，生成 {len(embeddings)} 个向量")
    print(f"   ✓ 向量维度: {len(embeddings[0])}")
    
    # 测试embed_query
    query_embedding = mock_embeddings.embed_query("测试查询")
    print(f"   ✓ embed_query成功")
    print(f"   ✓ 查询向量维度: {len(query_embedding)}")
except Exception as e:
    print(f"   ✗ MockEmbeddings测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

# 2. 跳过Chroma.from_texts测试，直接测试自定义VectorStore
print("\n2. 跳过Chroma.from_texts测试，直接测试自定义VectorStore...")

# 3. 测试VectorStore类
print("\n3. 测试VectorStore类...")
try:
    vector_store = VectorStore(use_mock=True)
    vector_store.add_texts(test_texts)
    print(f"   ✓ VectorStore.add_texts成功")
    
    # 测试相似性搜索
    results = vector_store.similarity_search("测试查询", k=1)
    print(f"   ✓ VectorStore.similarity_search成功，返回 {len(results)} 个结果")
except Exception as e:
    print(f"   ✗ VectorStore测试失败: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== 调试结束 ===")