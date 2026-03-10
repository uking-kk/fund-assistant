from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.fund_api import FundAPI

router = APIRouter()


class SearchRequest(BaseModel):
    keyword: str


class FundInfo(BaseModel):
    code: str
    name: str
    type: Optional[str] = None
    manager: Optional[str] = None
    scale: Optional[float] = None
    returns: Optional[dict] = None
    risk_level: Optional[str] = None


@router.post("/search")
async def search_fund(request: SearchRequest):
    """搜索基金"""
    api = FundAPI()
    results = await api.search_fund(request.keyword)
    return {"code": 200, "data": results}


@router.get("/detail/{fund_code}")
async def get_fund_detail(fund_code: str):
    """获取基金详情"""
    api = FundAPI()
    detail = await api.get_fund_detail(fund_code)
    return {"code": 200, "data": detail}


@router.get("/netvalue/{fund_code}")
async def get_fund_netvalue(fund_code: str, size: int = 30):
    """获取基金净值历史"""
    api = FundAPI()
    results = await api.get_fund_net_value(fund_code, size)
    return {"code": 200, "data": results}
