from functools import lru_cache

from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL, LLM_TEMPERATURE, validate_config


@lru_cache(maxsize=1)
def get_llm():
    validate_config()
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=LLM_TEMPERATURE,
    )