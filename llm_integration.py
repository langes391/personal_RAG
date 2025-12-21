from openai import OpenAI
from openai import APITimeoutError, APIError
import os
import time
import logging
from dotenv import load_dotenv
from config import LLM_MODEL, BASE_URL, TEMPERATURE, MAX_TOKENS, MAX_RETRIES

# 加载.env文件
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMIntegration:
    def __init__(self, use_fallback=True):
        """初始化LLM集成"""
        self.use_fallback = use_fallback
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # 只有当API密钥存在时才初始化OpenAI客户端
        if self.openai_api_key:
            try:
                # 使用DeepSeek API配置
                self.client = OpenAI(
                    api_key=self.openai_api_key,
                    base_url=BASE_URL,
                    timeout=30  # 设置30秒超时
                )
                logger.info(f"DeepSeek客户端初始化成功，base_url: {BASE_URL}")
            except Exception as e:
                logger.error(f"DeepSeek客户端初始化失败: {str(e)}")
                self.client = None
        else:
            logger.warning("未设置OPENAI_API_KEY，将使用本地回退机制")
            self.client = None
    
    def generate_answer(self, query, context, max_retries=None):
        """根据查询和上下文生成答案，支持重试机制"""
        # 使用配置文件中的重试次数，或者传入的重试次数
        retry_count = max_retries if max_retries is not None else MAX_RETRIES
        
        # 构建提示词
        prompt = self._build_prompt(query, context)
        
        # 如果没有DeepSeek客户端，使用回退机制
        if not self.client and self.use_fallback:
            return self._fallback_generate_answer(query, context)
        
        # 尝试调用DeepSeek API，支持重试
        for attempt in range(retry_count + 1):
            try:
                logger.info(f"尝试调用DeepSeek API (第 {attempt + 1}/{retry_count + 1} 次)")
                
                # 调用DeepSeek API
                response = self.client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[
                        {"role": "system", "content": "你是一个知识问答助手，根据提供的上下文回答用户的问题。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS
                )
                
                answer = response.choices[0].message.content.strip()
                logger.info(f"DeepSeek API调用成功，返回答案: {answer[:50]}...")
                return answer
                
            except APITimeoutError:
                logger.error(f"API请求超时 (第 {attempt + 1}/{retry_count + 1} 次)")
                if attempt == retry_count:
                    return f"请求超时，请稍后重试 (已尝试 {retry_count + 1} 次)"
                # 减少重试间隔，只等待1秒
                time.sleep(1)
            except APIError as e:
                logger.error(f"API错误 (第 {attempt + 1}/{retry_count + 1} 次): {str(e)}")
                if attempt == retry_count:
                    return f"API错误: {str(e)}"
                time.sleep(1)
            except Exception as e:
                logger.error(f"发生未知错误 (第 {attempt + 1}/{retry_count + 1} 次): {str(e)}")
                if attempt == retry_count:
                    return f"发生错误: {str(e)}"
                time.sleep(1)
    
    def _fallback_generate_answer(self, query, context):
        """本地回退生成答案机制"""
        logger.info("使用本地回退机制生成答案")
        
        # 简单的基于关键词匹配的回退机制
        context_str = "\n".join(context)
        
        # 提取关键词
        query_keywords = query.lower().split()
        context_lower = context_str.lower()
        
        # 计算匹配的关键词数量
        matched_keywords = [keyword for keyword in query_keywords if keyword in context_lower]
        
        if matched_keywords:
            return f"根据上下文，我找到了与 '{', '.join(matched_keywords)}' 相关的信息，但由于无法连接到OpenAI API，无法生成详细答案。\n\n上下文片段：{context_str[:200]}..."
        else:
            return "根据提供的上下文无法回答该问题 (使用本地回退机制)"
    
    def _build_prompt(self, query, context):
        """构建提示词"""
        context_str = "\n".join(context)
        
        prompt = f"上下文信息：\n{context_str}\n\n用户问题：{query}\n\n请根据上下文信息回答用户的问题，不要添加任何上下文之外的信息。如果上下文没有相关信息，请回答'根据提供的上下文无法回答该问题'。"
        
        return prompt