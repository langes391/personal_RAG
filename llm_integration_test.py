from unittest.mock import patch, MagicMock
from llm_integration import LLMIntegration

class TestLLMIntegration:
    def setup_method(self):
        """在每个测试方法前设置"""
        self.llm_integration = LLMIntegration()
    
    def build_prompt_test(self):
        """测试构建提示词功能"""
        # 准备测试数据
        query = "什么是Python？"
        context = ["Python是一种编程语言", "Python是开源的"]
        
        # 测试私有方法_build_prompt
        prompt = self.llm_integration._build_prompt(query, context)
        
        # 验证提示词构建结果
        assert "上下文信息" in prompt
        assert "Python是一种编程语言" in prompt
        assert "什么是Python？" in prompt
    
    @patch('openai.OpenAI')
    def generate_answer_test(self, mock_openai):
        """测试生成答案功能"""
        # 配置mock
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = "这是测试生成的答案"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # 准备测试数据
        query = "测试问题"
        context = ["测试上下文1", "测试上下文2"]
        
        # 测试生成答案
        result = self.llm_integration.generate_answer(query, context)
        
        # 验证结果
        assert result == "这是测试生成的答案"
        
        # 验证OpenAI API是否被正确调用
        mock_openai.return_value.chat.completions.create.assert_called_once()
    
    @patch('openai.OpenAI')
    def generate_answer_with_empty_context_test(self, mock_openai):
        """测试使用空上下文生成答案"""
        # 配置mock
        mock_response = MagicMock()
        mock_response.choices[0].message.content.strip.return_value = "根据提供的上下文无法回答该问题"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # 准备测试数据
        query = "测试问题"
        context = []
        
        # 测试生成答案
        result = self.llm_integration.generate_answer(query, context)
        
        # 验证结果
        assert "根据提供的上下文无法回答该问题" in result