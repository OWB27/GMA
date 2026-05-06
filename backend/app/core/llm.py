from langchain_openai import ChatOpenAI

from app.core.config import get_settings


def get_chat_model() -> ChatOpenAI:
    settings = get_settings()
    if not settings.llm_api_key:
        raise ValueError("LLM_API_KEY is required to create a chat model.")

    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        temperature=settings.llm_temperature,
    )
