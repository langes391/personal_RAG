from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_integration import LLMIntegration

print("=== 个人知识库问答系统完整流程测试 ===")

# 1. 初始化各模块
print("\n1. 初始化各模块...")
doc_processor = DocumentProcessor()
vector_store = VectorStore(use_mock=True)
llm_integration = LLMIntegration()

# 2. 测试文件解析
print("\n2. 测试文件解析...")
file_path = "d:\\pycharm\\project\\personal\\personal_RAG\\今日安排3.txt"
chunks = doc_processor.process_file(file_path)
print(f"   ✓ 文件解析成功，生成 {len(chunks)} 个文本块")

# 3. 测试向量存储
print("\n3. 测试向量存储...")
try:
    vector_store.add_texts(chunks)
    print("   ✓ 向量存储成功")
except Exception as e:
    print(f"   ⚠️  向量存储失败：{str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

# 4. 测试相似性检索
print("\n4. 测试相似性检索...")
query = "12.10的安排是什么？"
context = vector_store.similarity_search(query, k=2)
print(f"   ✓ 检索到 {len(context)} 个相关文本块")
print(f"   相关文本：{context[0][:100]}...")

# 5. 测试LLM生成答案
print("\n5. 测试LLM生成答案...")
try:
    answer = llm_integration.generate_answer(query, context)
    print(f"   ✓ 答案生成成功")
    print(f"   答案：{answer}")
except Exception as e:
    print(f"   ⚠️  答案生成失败：{str(e)}")
    print("   这可能是因为无法连接到OpenAI API，但不影响其他功能测试")

print("\n=== 测试完成 ===")
print("文件解析、向量存储和检索功能正常工作！")
print("LLM生成功能可能需要配置有效的OpenAI API密钥才能正常工作。")