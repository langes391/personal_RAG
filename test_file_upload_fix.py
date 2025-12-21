import os
import sys
import tempfile

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import KnowledgeBaseQA
from config import UPLOAD_DIR

def test_file_upload_fix():
    """测试文件上传修复效果"""
    print("=== 测试文件上传修复效果 ===")
    
    # 1. 准备测试环境
    print("\n1. 准备测试环境...")
    
    # 确保上传目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 创建一个测试文件
    test_content = "测试文件内容，用于验证文件上传修复"
    test_file_path = os.path.join(UPLOAD_DIR, "test_fix.txt")
    
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print(f"   创建了测试文件: {test_file_path}")
    
    # 2. 初始化应用，检查files_uploaded状态
    print("\n2. 初始化应用，检查files_uploaded状态...")
    
    # 模拟Streamlit会话状态
    import streamlit as st
    if "files_uploaded" in st.session_state:
        del st.session_state["files_uploaded"]
    
    # 初始化应用
    app = KnowledgeBaseQA()
    
    # 检查files_uploaded状态
    print(f"   应用初始化后files_uploaded状态: {st.session_state.files_uploaded}")
    
    # 3. 模拟上传文件
    print("\n3. 模拟上传文件...")
    
    # 直接调用add_texts方法，模拟文件处理
    app.vector_store.add_texts([test_content])
    
    # 设置会话状态
    st.session_state.files_uploaded = True
    
    # 检查会话状态
    print(f"   上传文件后files_uploaded状态: {st.session_state.files_uploaded}")
    
    # 4. 模拟刷新页面
    print("\n4. 模拟刷新页面...")
    
    # 清除会话状态
    del st.session_state["files_uploaded"]
    
    # 重新初始化应用
    app2 = KnowledgeBaseQA()
    
    # 检查会话状态
    print(f"   刷新页面后files_uploaded状态: {st.session_state.files_uploaded}")
    
    # 5. 测试向量存储是否有数据
    print("\n5. 测试向量存储是否有数据...")
    print(f"   向量存储中文本块数量: {len(app2.vector_store.texts)}")
    
    # 6. 清理测试环境
    print("\n6. 清理测试环境...")
    
    # 删除测试文件
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"   删除了测试文件: {test_file_path}")
    
    # 重置向量存储
    app2.vector_store.reset()
    
    # 7. 验证修复效果
    print("\n7. 验证修复效果...")
    
    # 检查最终结果
    if st.session_state.files_uploaded:
        print("✅ 修复成功！已上传的文件能够被正确识别，无需重复上传。")
        print("✅ 会话状态管理正常，刷新页面后仍能识别已上传的文件。")
        return True
    else:
        print("❌ 修复失败！已上传的文件未能被正确识别。")
        return False

if __name__ == "__main__":
    test_file_upload_fix()
    print("\n=== 测试完成 ===")