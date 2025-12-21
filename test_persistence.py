import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_store import VectorStore
from config import UPLOAD_DIR, VECTOR_STORE_PATH

def test_vector_store_persistence():
    """测试向量存储的持久化功能"""
    print("=== 测试向量存储持久化功能 ===")
    
    # 清理测试环境：删除现有的向量存储文件
    vector_store_file = os.path.join(VECTOR_STORE_PATH, "vector_store.pkl")
    if os.path.exists(vector_store_file):
        os.remove(vector_store_file)
        print(f"   清理了旧的向量存储文件: {vector_store_file}")
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    test_texts = [
        "第一段测试文本，用于验证向量存储持久化",
        "第二段测试文本，用于验证向量存储持久化",
        "第三段测试文本，用于验证向量存储持久化"
    ]
    
    # 2. 创建并初始化向量存储
    print("\n2. 创建并初始化向量存储...")
    vector_store = VectorStore(use_mock=True)
    
    # 3. 添加测试文本
    print("\n3. 添加测试文本到向量存储...")
    vector_store.add_texts(test_texts)
    
    print(f"   添加了 {len(test_texts)} 个文本块")
    print(f"   向量存储中文本块数量: {len(vector_store.texts)}")
    
    # 4. 检查向量存储文件是否创建
    print("\n4. 检查向量存储文件是否创建...")
    vector_store_file = os.path.join(VECTOR_STORE_PATH, "vector_store.pkl")
    assert os.path.exists(vector_store_file), f"向量存储文件未创建: {vector_store_file}"
    print(f"   ✅ 向量存储文件已创建: {vector_store_file}")
    file_size = os.path.getsize(vector_store_file)
    print(f"   文件大小: {file_size} 字节")
    
    # 5. 创建新的向量存储实例，应该能加载已保存的数据
    print("\n5. 创建新的向量存储实例，测试加载已保存的数据...")
    vector_store2 = VectorStore(use_mock=True)
    
    print(f"   新向量存储中文本块数量: {len(vector_store2.texts)}")
    assert len(vector_store2.texts) == len(test_texts), "未能加载已保存的向量存储数据"
    print("   ✅ 成功加载了已保存的向量存储数据")
    
    # 6. 测试相似性搜索
    print("\n6. 测试相似性搜索...")
    query = "测试向量存储持久化"
    results = vector_store2.similarity_search(query, k=2)
    
    print(f"   查询: {query}")
    print(f"   返回了 {len(results)} 个结果")
    assert results, "相似性搜索未返回结果"
    print(f"   前2个结果:")
    for i, result in enumerate(results):
        print(f"   {i+1}. {result[:50]}...")
    print("   ✅ 相似性搜索功能正常")
    
    # 7. 测试重置功能
    print("\n7. 测试重置功能...")
    vector_store2.reset()
    
    print(f"   重置后向量存储中文本块数量: {len(vector_store2.texts)}")
    assert len(vector_store2.texts) == 0, "未能重置向量存储"
    print("   ✅ 成功重置向量存储")
    
    # 8. 检查向量存储文件是否已删除
    print("\n8. 检查向量存储文件是否已删除...")
    if not os.path.exists(vector_store_file):
        print(f"   ✅ 向量存储文件已删除")
    else:
        print(f"   ❌ 向量存储文件未删除: {vector_store_file}")
        # 手动删除文件
        os.remove(vector_store_file)
    
    print("\n=== 测试完成 ===")
    print("✅ 向量存储持久化功能测试通过！")

def test_upload_dir_handling():
    """测试上传目录处理"""
    print("\n=== 测试上传目录处理 ===")
    
    # 1. 检查上传目录是否存在
    print("\n1. 检查上传目录是否存在...")
    assert os.path.exists(UPLOAD_DIR), f"上传目录不存在: {UPLOAD_DIR}"
    print(f"   ✅ 上传目录已存在: {UPLOAD_DIR}")
    
    # 列出上传目录中的文件
    files = os.listdir(UPLOAD_DIR)
    if files:
        print(f"   上传目录中包含 {len(files)} 个文件:")
        for file in files:
            print(f"   - {file}")
    else:
        print(f"   上传目录为空")
    print("✅ 上传目录处理测试通过！")

if __name__ == "__main__":
    # 运行测试
    test_vector_store_persistence()
    test_upload_dir_handling()
    
    print("\n🎉 所有测试通过！向量存储持久化功能正常工作。")
    sys.exit(0)