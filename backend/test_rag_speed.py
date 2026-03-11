import time
from app.core.rag import get_rag_retriever

print("测试RAG检索性能")
print("=" * 60)

rag = get_rag_retriever()

# 测试RAG检索
print("\n测试RAG检索...")
start = time.time()
docs = rag.retrieve("什么是基金定投", k=2)
rag_time = time.time() - start
print(f"RAG检索时间: {rag_time*1000:.0f}ms")
print(f"检索结果: {len(docs)}条")
print(f"内容: {docs}")

print("\n测试完成！")
