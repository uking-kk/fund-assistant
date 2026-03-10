from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api import chat, fund

settings = get_settings()

app = FastAPI(
    title="基金智能助手 API",
    description="基于大语言模型的基金投资问答助手",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(fund.router, prefix="/api/fund", tags=["fund"])


@app.get("/")
async def root():
    return {"message": "基金智能助手 API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
