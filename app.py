import streamlit as st
import os
import tempfile
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_integration import LLMIntegration
from config import APP_TITLE, APP_DESCRIPTION, SUPPORTED_FILE_TYPES, UPLOAD_DIR

class KnowledgeBaseQA:
    def __init__(self):
        """初始化知识库问答系统"""
        self.document_processor = DocumentProcessor()
        # 使用真实的嵌入模型，确保向量存储生成有意义的嵌入
        self.vector_store = VectorStore(use_mock=False)
        self.llm_integration = LLMIntegration()
        
        # 初始化会话状态
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # 检查是否已有上传的文件或向量存储数据
        has_files = False
        
        # 检查上传目录是否有文件
        if os.path.exists(UPLOAD_DIR) and os.listdir(UPLOAD_DIR):
            has_files = True
        
        # 检查向量存储是否有数据
        if getattr(self.vector_store, 'texts', None) and len(self.vector_store.texts) > 0:
            has_files = True
        
        # 初始化files_uploaded状态
        if "files_uploaded" not in st.session_state:
            st.session_state.files_uploaded = has_files
    
    def run(self):
        """运行应用"""
        # 设置页面标题和图标
        st.set_page_config(
            page_title=APP_TITLE,
            page_icon="📚",
            layout="wide"
        )
        
        # 确保上传目录存在
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # 每次运行时检查是否已有上传的文件或向量存储数据
        has_files = False
        
        # 检查上传目录是否有文件
        if os.path.exists(UPLOAD_DIR) and os.listdir(UPLOAD_DIR):
            has_files = True
        
        # 检查向量存储是否有数据
        if getattr(self.vector_store, 'texts', None) and len(self.vector_store.texts) > 0:
            has_files = True
        
        # 更新files_uploaded状态
        st.session_state.files_uploaded = has_files
        
        # 应用标题和说明
        st.title(APP_TITLE)
        st.write(APP_DESCRIPTION)
        
        # 创建侧边栏
        with st.sidebar:
            st.header("文件上传")
            
            # 文件上传组件
            uploaded_files = st.file_uploader(
                "上传文档",
                type=[ext[1:] for ext in SUPPORTED_FILE_TYPES],
                accept_multiple_files=True
            )
            
            # 处理上传的文件
            if uploaded_files:
                with st.spinner("正在处理文件..."):
                    all_chunks = []
                    for uploaded_file in uploaded_files:
                        # 保存文件到持久化目录
                        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        
                        # 处理文件
                        chunks = self.document_processor.process_file(file_path)
                        all_chunks.extend(chunks)
                    
                    try:
                        # 添加到向量存储
                        self.vector_store.add_texts(all_chunks)
                        st.session_state.files_uploaded = True
                        st.success(f"成功处理 {len(uploaded_files)} 个文件，生成 {len(all_chunks)} 个文本块")
                    except Exception as e:
                        st.error(f"文件处理失败：{str(e)}")
            
            # 显示已上传的文件
            uploaded_file_list = os.listdir(UPLOAD_DIR)
            if uploaded_file_list:
                st.subheader("已上传的文件")
                for file_name in uploaded_file_list:
                    st.write(f"📄 {file_name}")
                
                # 清除已上传文件按钮
                if st.button("清除已上传文件", type="secondary"):
                    # 删除所有已上传文件
                    for file_name in uploaded_file_list:
                        file_path = os.path.join(UPLOAD_DIR, file_name)
                        os.remove(file_path)
                    st.success("已清除所有已上传文件")
                    st.rerun()
            
            # 清除按钮
            if st.button("清除所有", type="primary"):
                self.reset()
        
        # 聊天窗口
        st.header("聊天窗口")
        
        # 显示聊天历史
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # 用户输入
        if prompt := st.chat_input("请输入您的问题..."):
            # 检查是否已上传文件
            if not st.session_state.files_uploaded:
                st.error("请先上传文档")
                return
            
            # 添加用户消息到聊天历史
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 生成回答
            with st.chat_message("assistant"):
                with st.spinner("正在生成答案..."):
                    # 检索相关上下文
                    context = self.vector_store.similarity_search(prompt)
                    
                    # 生成答案
                    answer = self.llm_integration.generate_answer(prompt, context)
                    
                    # 显示答案
                    st.markdown(answer)
            
            # 添加助手回答到聊天历史
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
    
    def reset(self):
        """重置应用状态"""
        # 重置向量存储
        self.vector_store.reset()
        
        # 清空聊天历史
        st.session_state.chat_history = []
        st.session_state.files_uploaded = False
        
        # 刷新页面
        st.rerun()

if __name__ == "__main__":
    app = KnowledgeBaseQA()
    app.run()