"""LLM and chain setup"""
import os
from functools import lru_cache
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from app.core.ai.prompts import get_qa_prompt_template
from app.core.kb.retriever import get_retriever

load_dotenv()


@lru_cache()
def get_llm():
    """Get cached LLM instance"""
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "gpt-4"),
        temperature=0.6,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


@lru_cache()
def get_qa_chain():
    """Get cached RetrievalQA chain"""
    llm = get_llm()
    retriever = get_retriever()
    prompt_template = get_qa_prompt_template()
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type='stuff',
        chain_type_kwargs={'prompt': prompt_template}
    )


def generate_ai_response(user_text: str) -> str:
    """Generate AI response for user text"""
    chain = get_qa_chain()
    return chain.run(user_text)

