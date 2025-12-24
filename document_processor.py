import os
from PyPDF2 import PdfReader
from docx import Document
import markdown
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
    
    def process_file(self, file_path):
        """处理不同类型的文件，返回文本块列表"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # 读取文件内容
        if file_extension == ".pdf":
            text = self._read_pdf(file_path)
        elif file_extension == ".txt":
            text = self._read_txt(file_path)
        elif file_extension == ".docx":
            text = self._read_docx(file_path)
        elif file_extension == ".md":
            text = self._read_markdown(file_path)
        elif file_extension == ".html" or file_extension == ".htm":
            text = self._read_html(file_path)
        else:
            raise ValueError(f"不支持的文件类型: {file_extension}")
        
        # 确保文本不为空
        if not text or text.strip() == "":
            # 如果文本为空，返回一个默认文本块
            return ["文件内容为空"]
        
        # 分割文本
        chunks = self._split_text(text)
        
        # 确保返回的文本块列表不为空
        if not chunks:
            return ["文件处理成功，但未生成文本块"]
        
        return chunks
    
    def _read_pdf(self, file_path):
        """读取PDF文件内容"""
        text = ""
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    
    def _read_txt(self, file_path):
        """读取TXT文件内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _read_docx(self, file_path):
        """读取DOCX文件内容"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _read_markdown(self, file_path):
        """读取Markdown文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                md_text = f.read()
            # 将Markdown转换为HTML
            html = markdown.markdown(md_text)
            # 使用BeautifulSoup提取纯文本
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text()
        except Exception as e:
            # 如果解析失败，直接返回原始内容
            print(f"解析Markdown时出错: {e}")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    
    def _read_html(self, file_path):
        """读取HTML文件内容"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()
            # 使用BeautifulSoup提取纯文本
            soup = BeautifulSoup(html, 'html.parser')
            # 移除脚本和样式标签
            for script in soup(['script', 'style']):
                script.decompose()
            # 获取文本并清理空白
            text = ' '.join(soup.stripped_strings)
            return text
        except Exception as e:
            print(f"解析HTML时出错: {e}")
            return "无法解析HTML文件"
    
    def _split_text(self, text):
        """将文本分割成块"""
        # 如果文本为空，返回一个包含空字符串的列表，避免生成0个文本块
        if not text or text.strip() == "":
            return [" "]
        return self.text_splitter.split_text(text)