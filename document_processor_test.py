import os
import tempfile
from document_processor import DocumentProcessor

class TestDocumentProcessor:
    def setup_method(self):
        """在每个测试方法前设置"""
        self.processor = DocumentProcessor()
    
    def read_txt_test(self):
        """测试读取TXT文件"""
        # 创建临时TXT文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w', encoding='utf-8') as temp_file:
            temp_file.write("这是一个测试TXT文件\n包含多行文本")
            temp_file_path = temp_file.name
        
        try:
            # 测试私有方法_read_txt
            result = self.processor._read_txt(temp_file_path)
            assert "这是一个测试TXT文件" in result
            assert "包含多行文本" in result
        finally:
            # 删除临时文件
            os.unlink(temp_file_path)
    
    def split_text_test(self):
        """测试文本分块功能"""
        # 创建长文本
        long_text = "测试文本" * 1000
        
        # 测试文本分块
        chunks = self.processor._split_text(long_text)
        
        # 验证分块结果
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def process_file_unsupported_type_test(self):
        """测试处理不支持的文件类型"""
        # 创建临时不支持的文件类型
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(b"col1,col2\nvalue1,value2")
            temp_file_path = temp_file.name
        
        try:
            # 测试处理不支持的文件类型
            self.processor.process_file(temp_file_path)
        except ValueError as e:
            assert "不支持的文件类型" in str(e)
        finally:
            # 删除临时文件
            os.unlink(temp_file_path)