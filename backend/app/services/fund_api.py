import httpx
from typing import List, Dict, Optional
import re
import json


class FundAPI:
    """
    天天基金API封装（东方财富）
    
    免费接口，无需API Key
    - 基金搜索: 通过基金列表本地搜索
    - 基金详情: fundgz.1234567.com.cn
    - 基金净值: api.fund.eastmoney.com
    """
    
    FUND_LIST_URL = "http://fund.eastmoney.com/js/fundcode_search.js"
    FUND_DETAIL_URL = "http://fundgz.1234567.com.cn/js/{fund_code}.js"
    FUND_NET_VALUE_URL = "http://api.fund.eastmoney.com/f10/lsjz"
    
    _fund_list_cache: Optional[List[Dict]] = None
    
    def __init__(self, timeout: int = 10):
        self.client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True
        )
    
    async def close(self):
        """关闭客户端连接"""
        await self.client.aclose()
    
    async def _get_all_funds(self) -> List[Dict]:
        """
        获取所有基金列表（带缓存）
        
        Returns:
            基金列表 [{code, name, type, pinyin}]
        """
        if self._fund_list_cache is not None:
            return self._fund_list_cache
        
        try:
            response = await self.client.get(self.FUND_LIST_URL)
            response.raise_for_status()
            
            content = response.text
            
            match = re.search(r'var r = \[(.*?)\];', content, re.DOTALL)
            if not match:
                return []
            
            funds_str = '[' + match.group(1) + ']'
            funds_data = json.loads(funds_str)
            
            self._fund_list_cache = [
                {
                    "code": fund[0],
                    "name": fund[2],
                    "type": fund[3],
                    "pinyin": fund[1]
                }
                for fund in funds_data
            ]
            
            return self._fund_list_cache
            
        except Exception as e:
            print(f"获取基金列表失败: {e}")
            return []
    
    async def search_fund(self, keyword: str) -> List[Dict]:
        """
        搜索基金
        
        Args:
            keyword: 搜索关键词（基金名称、代码或拼音）
            
        Returns:
            基金列表
        """
        try:
            all_funds = await self._get_all_funds()
            
            keyword_lower = keyword.lower()
            
            results = []
            for fund in all_funds:
                if (keyword_lower in fund["code"] or
                    keyword_lower in fund["name"].lower() or
                    keyword_lower in fund["pinyin"].lower()):
                    results.append({
                        "code": fund["code"],
                        "name": fund["name"],
                        "type": fund["type"]
                    })
                    
                    if len(results) >= 10:
                        break
            
            return results
            
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
            url = self.FUND_DETAIL_URL.format(fund_code=fund_code)
            response = await self.client.get(url)
            response.raise_for_status()
            
            content = response.text
            
            match = re.search(r'jsonpgz\((.*?)\);', content)
            if not match:
                return {}
            
            data = json.loads(match.group(1))
            
            if data.get("fundcode") != fund_code:
                return {}
            
            return {
                "code": fund_code,
                "name": data.get("name"),
                "type": data.get("fundtype"),
                "net_value": data.get("gsz"),
                "net_value_date": data.get("gztime"),
                "expect_growth": data.get("gszzl"),
                "yesterday_value": data.get("dwjz"),
                "yesterday_date": data.get("jzrq"),
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
            params = {
                "fundCode": fund_code,
                "pageIndex": 1,
                "pageSize": size,
                "startDate": "",
                "endDate": ""
            }
            
            headers = {
                "Referer": "http://fund.eastmoney.com/"
            }
            
            response = await self.client.get(
                self.FUND_NET_VALUE_URL,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("ErrCode") != 0:
                return []
            
            lsjz_list = data.get("Data", {}).get("LSJZList", [])
            
            return [
                {
                    "date": item.get("FSRQ"),
                    "net_value": item.get("DWJZ"),
                    "accumulated_value": item.get("LJJZ"),
                    "growth_rate": item.get("JZZZL")
                }
                for item in lsjz_list
            ]
            
        except Exception as e:
            print(f"获取基金净值失败: {e}")
            return []


fund_api = FundAPI()
