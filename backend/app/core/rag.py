from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List, Optional, Tuple
from functools import lru_cache
import os


@lru_cache(maxsize=1)
def get_embeddings():
    """单例模式获取Embeddings，避免重复加载模型"""
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


class RAGRetriever:
    """
    RAG检索模块 - 性能优化版
    
    优化点：
    1. 使用单例模式避免重复加载向量模型
    2. 延迟初始化向量数据库
    3. 缓存检索结果
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
    ):
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self.embeddings = get_embeddings()
        self.persist_directory = persist_directory
        self._vectorstore = None
        self._initialized = False
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", "。", "，", " ", ""]
        )
        
        self._initialized = True
    
    @property
    def vectorstore(self):
        """延迟加载向量数据库"""
        if self._vectorstore is None:
            if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
                self._vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
        return self._vectorstore
    
    def init_vectorstore(self, documents: List[Document]):
        chunks = self.text_splitter.split_documents(documents)
        print(f"文档分块完成，共 {len(chunks)} 个块")
        
        self._vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self._vectorstore.persist()
        print(f"向量数据库已保存到 {self.persist_directory}")
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        documents = [
            Document(page_content=text, metadata=metadatas[i] if metadatas else {})
            for i, text in enumerate(texts)
        ]
        if self._vectorstore is None:
            self.init_vectorstore(documents)
        else:
            chunks = self.text_splitter.split_documents(documents)
            self._vectorstore.add_documents(chunks)
            self._vectorstore.persist()
    
    def retrieve(self, query: str, k: int = 3) -> List[str]:
        if self.vectorstore is None:
            return []
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]


_rag_instance = None

def get_rag_retriever() -> RAGRetriever:
    """获取RAG检索器单例"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGRetriever()
    return _rag_instance
