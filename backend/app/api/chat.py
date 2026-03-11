from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.agent import get_agent
import json

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str = None


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    对话接口 - 流式输出
    使用Server-Sent Events (SSE)实现流式传输
    """
    
    async def generate():
        try:
            agent = await get_agent()
            
            async for chunk in agent.chat(request.message):
                data = json.dumps({
                    "content": chunk,
                    "done": False
                }, ensure_ascii=False)
                yield f"data: {data}\n\n"
            
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            
        except Exception as e:
            error_data = json.dumps({
                "error": str(e),
                "done": True
            }, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
