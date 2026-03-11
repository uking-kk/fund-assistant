import asyncio
import time
from app.services.fund_api import fund_api

async def test_fund_api_speed():
    print("测试基金API响应速度")
    print("=" * 60)
    
    # 测试搜索基金
    print("\n测试搜索基金...")
    start = time.time()
    results = await fund_api.search_fund("招商白酒")
    search_time = time.time() - start
    print(f"搜索时间: {search_time*1000:.0f}ms")
    print(f"搜索结果: {results[:2]}")
    
    # 测试获取基金详情
    if results:
        code = results[0]['code']
        print(f"\n测试获取基金详情 ({code})...")
        start = time.time()
        detail = await fund_api.get_fund_detail(code)
        detail_time = time.time() - start
        print(f"详情时间: {detail_time*1000:.0f}ms")
        print(f"详情: {detail}")
    
    # 测试获取基金净值
    if results:
        code = results[0]['code']
        print(f"\n测试获取基金净值 ({code})...")
        start = time.time()
        net_value = await fund_api.get_fund_net_value(code, size=10)
        net_value_time = time.time() - start
        print(f"净值时间: {net_value_time*1000:.0f}ms")
        print(f"净值数据: {len(net_value)}条")
    
    await fund_api.close()

if __name__ == "__main__":
    asyncio.run(test_fund_api_speed())
