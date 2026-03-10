from typing import AsyncGenerator
from app.core.rag import get_rag_retriever
from app.services.llm import llm_service
from app.services.fund_api import fund_api
import json
import re


class FundAssistantAgent:
    """
    基金助手Agent - 性能优化版
    
    优化点：
    1. 使用单例模式避免重复初始化
    2. 复用RAG和API实例
    3. 简化意图识别逻辑
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.rag = get_rag_retriever()
        self._initialized = True
    
    async def chat(self, question: str) -> AsyncGenerator[str, None]:
        intent = self._detect_intent(question)
        
        if intent == "query":
            context = await self._fund_query(question)
            prompt = self._build_prompt(question, context, "query")
        elif intent == "recommend":
            context = await self._fund_recommend(question)
            prompt = self._build_prompt(question, context, "recommend")
        else:
            context = self._knowledge_qa(question)
            prompt = self._build_prompt(question, context, "qa")
        
        messages = [{"role": "user", "content": prompt}]
        
        async for chunk in llm_service.chat_stream(messages):
            yield chunk
    
    def _detect_intent(self, question: str) -> str:
        if any(kw in question for kw in ["查", "查询", "净值", "收益", "怎么样", "这只", "代码"]):
            return "query"
        if any(kw in question for kw in ["推荐", "找", "选", "适合", "建议"]):
            return "recommend"
        return "qa"
    
    def _build_prompt(self, question: str, context: str, intent: str) -> str:
        base = """你是一个专业的基金投资助手。请简洁专业地回答用户问题。
如果提供了数据，请用列表或表格展示。"""
        
        if intent == "query":
            return f"{base}\n\n用户问题：{question}\n\n基金数据：\n{context}\n\n请基于数据回答："
        return f"{base}\n\n用户问题：{question}\n\n相关知识：\n{context}\n\n请回答："
    
    def _knowledge_qa(self, question: str) -> str:
        docs = self.rag.retrieve(question, k=2)
        return "\n\n".join(docs) if docs else "请根据你的知识回答。"
    
    async def _fund_query(self, question: str) -> str:
        match = re.search(r'\d{6}', question)
        if match:
            detail = await fund_api.get_fund_detail(match.group())
            if detail:
                return json.dumps(detail, ensure_ascii=False, indent=2)
        
        keywords = re.sub(r'[查询一下的基金]', '', question).strip()
        if keywords:
            results = await fund_api.search_fund(keywords)
            if results:
                detail = await fund_api.get_fund_detail(results[0].get("code"))
                if detail:
                    return json.dumps(detail, ensure_ascii=False, indent=2)
        return "未找到相关基金信息"
    
    async def _fund_recommend(self, question: str) -> str:
        if "稳健" in question or "债券" in question:
            fund_type = "债券型"
        elif "成长" in question or "股票" in question:
            fund_type = "股票型"
        else:
            fund_type = "混合型"
        
        results = await fund_api.search_fund(fund_type)
        if results:
            return json.dumps(results[:3], ensure_ascii=False, indent=2)
        return "暂无推荐结果"


_agent_instance = None

def get_agent() -> FundAssistantAgent:
    """获取Agent单例"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = FundAssistantAgent()
    return _agent_instance
