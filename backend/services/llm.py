from openai import OpenAI
from app.config import get_settings
from typing import AsyncGenerator
import os

settings = get_settings()


class LLMService:
    """
    LLM服务 - 使用火山方舟API
    """
    
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.ARK_BASE_URL,
            api_key=settings.ARK_API_KEY,
        )
        self.model = settings.ARK_MODEL
    
    def chat(self, messages: list, stream: bool = False):
        """
        对话接口
        
        Args:
            messages: 消息列表
            stream: 是否流式输出
            
        Returns:
            模型响应
        """
        if stream:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
    
    async def chat_stream(self, messages: list) -> AsyncGenerator[str, None]:
        """
        流式对话
        
        Args:
            messages: 消息列表
            
        Yields:
            str: 流式输出的内容片段
        """
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    def simple_chat(self, prompt: str) -> str:
        """
        简单对话
        
        Args:
            prompt: 用户输入
            
        Returns:
            模型响应
        """
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages)


llm_service = LLMService()
