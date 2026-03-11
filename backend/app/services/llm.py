from openai import AsyncOpenAI
from app.config import get_settings
from typing import AsyncGenerator, List, Dict

settings = get_settings()


class LLMService:
    """
    LLM服务 - 使用火山方舟API（异步版本）
    
    使用 Chat API（兼容OpenAI格式）:
    - base_url: https://ark.cn-beijing.volces.com/api/v3
    - 端点: /chat/completions
    """
    
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.ARK_BASE_URL,
            api_key=settings.ARK_API_KEY,
        )
        self.model = settings.ARK_MODEL
    
    async def chat(self, messages: List[Dict], stream: bool = False):
        """
        对话接口
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            stream: 是否流式输出
            
        Returns:
            模型响应
        """
        if stream:
            return await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True
            )
        else:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
    
    async def chat_stream(self, messages: List[Dict]) -> AsyncGenerator[str, None]:
        """
        流式对话
        
        Args:
            messages: 消息列表
            
        Yields:
            str: 流式输出的内容片段
        """
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def simple_chat(self, prompt: str) -> str:
        """
        简单对话
        
        Args:
            prompt: 用户输入
            
        Returns:
            模型响应
        """
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages)


llm_service = LLMService()
