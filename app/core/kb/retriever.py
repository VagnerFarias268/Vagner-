"""LangChain retriever wrapper for Pinecone KB"""
from functools import lru_cache
from langchain.schema import BaseRetriever
from app.core.kb.manager import query


class RetrieverWrapper(BaseRetriever):
    """LangChain-compatible retriever wrapper"""
    
    def _get_relevant_documents(self, query_text: str, *, run_manager=None):
        return query(query_text, top_k=3)

    async def _aget_relevant_documents(self, query_text: str, *, run_manager=None):
        return query(query_text, top_k=3)


@lru_cache()
def get_retriever():
    """Get cached retriever instance"""
    return RetrieverWrapper()

