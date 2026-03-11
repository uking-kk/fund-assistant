import asyncio
import time
from openai import AsyncOpenAI

async def test_model_speed(model_name: str):
    print(f"\n测试模型: {model_name}")
    print("-" * 60)
    
    client = AsyncOpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="8d6d5097-f43b-4380-a31f-943736d99f65",
    )
    
    start_time = time.time()
    
    try:
        stream = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "你好"}],
            stream=True
        )
        
        first_chunk_time = None
        full_response = ""
        
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                if first_chunk_time is None:
                    first_chunk_time = time.time()
                    print(f"首字响应时间: {(first_chunk_time - start_time)*1000:.0f}ms")
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)
        
        total_time = time.time() - start_time
        print(f"\n总响应时间: {total_time*1000:.0f}ms")
        print(f"完整回复: {full_response}")
        
        return {
            "model": model_name,
            "first_chunk_time": (first_chunk_time - start_time) * 1000 if first_chunk_time else None,
            "total_time": total_time * 1000,
            "success": True
        }
        
    except Exception as e:
        print(f"\n错误: {e}")
        return {
            "model": model_name,
            "error": str(e),
            "success": False
        }
    finally:
        await client.close()

async def main():
    print("测试火山方舟API响应速度")
    print("=" * 60)
    
    models = [
        "doubao-seed-2-0-pro-260215",
        "doubao-seed-2-0-lite-260215"
    ]
    
    results = []
    for model in models:
        result = await test_model_speed(model)
        results.append(result)
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("-" * 60)
    for result in results:
        if result["success"]:
            print(f"{result['model']}:")
            print(f"  首字响应: {result['first_chunk_time']:.0f}ms")
            print(f"  总响应: {result['total_time']:.0f}ms")
        else:
            print(f"{result['model']}: 失败 - {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
