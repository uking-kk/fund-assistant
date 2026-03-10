import httpx
from typing import List, Dict, Optional


class FundAPI:
    """
    天天基金API封装
    
    API文档参考：
    - 基金搜索: POST /fund/search
    - 基金详情: POST /fund/detail
    - 基金净值: POST /fund/netValue
    """
    
    BASE_URL = "https://api.doctorxiong.club/v1"
    
    def __init__(self, timeout: int = 10):
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=timeout
        )
    
    async def close(self):
        """关闭客户端连接"""
        await self.client.aclose()
    
    async def search_fund(self, keyword: str) -> List[Dict]:
        """
        搜索基金
        
        Args:
            keyword: 搜索关键词（基金名称或代码）
            
        Returns:
            基金列表
        """
        try:
            response = await self.client.post(
                "/fund/search",
                json={"keyword": keyword}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") != 200:
                return []
            
            return data.get("data", [])
            
        except Exception as e:
            print(f"搜索基金失败: {e}")
            return []
    
    async def get_fund_detail(self, fund_code: str) -> Dict:
        """
        获取基金详情
        
        Args:
            fund_code: 基金代码（6位数字）
            
        Returns:
            基金详情信息
        """
        try:
            response = await self.client.post(
                "/fund/detail",
                json={"fundCode": fund_code}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") != 200:
                return {}
            
            raw_data = data.get("data", {})
            
            return {
                "code": fund_code,
                "name": raw_data.get("name"),
                "type": raw_data.get("fundType"),
                "manager": raw_data.get("managerName"),
                "company": raw_data.get("fundCompany"),
                "scale": raw_data.get("fundScale"),
                "establish_date": raw_data.get("establishDate"),
                "risk_level": raw_data.get("riskLevel"),
                "returns": {
                    "1w": raw_data.get("returnRate1w"),
                    "1m": raw_data.get("returnRate1m"),
                    "3m": raw_data.get("returnRate3m"),
                    "6m": raw_data.get("returnRate6m"),
                    "1y": raw_data.get("returnRate1y"),
                    "3y": raw_data.get("returnRate3y"),
                },
                "net_value": raw_data.get("netValue"),
                "net_value_date": raw_data.get("netValueDate"),
            }
            
        except Exception as e:
            print(f"获取基金详情失败: {e}")
            return {}
    
    async def get_fund_net_value(
        self, 
        fund_code: str,
        size: int = 30
    ) -> List[Dict]:
        """
        获取基金净值历史
        
        Args:
            fund_code: 基金代码
            size: 返回数据条数
            
        Returns:
            净值历史列表
        """
        try:
            response = await self.client.post(
                "/fund/netValue",
                json={
                    "fundCode": fund_code,
                    "size": size
                }
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") != 200:
                return []
            
            return data.get("data", [])
            
        except Exception as e:
            print(f"获取基金净值失败: {e}")
            return []


fund_api = FundAPI()
