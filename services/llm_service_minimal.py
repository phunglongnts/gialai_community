# Minimal LLM Service - không có f-string lỗi
import asyncio
from typing import Dict, List, Any, Optional


class LLMService:
    def __init__(self, model_name: str = "llama-3.2-3b-instruct"):
        self.model_name = model_name

    async def health_check(self) -> str:
        return "LLM not configured yet"

    async def search_restaurants(self, query: str, context: str) -> Dict[str, Any]:
        return {
            "response": f"Tìm kiếm: {query} (LLM chưa cấu hình)",
            "recommendations": [],
            "confidence_score": 0.0
        }

    async def chat_with_context(self, message: str, context: str, history=None) -> str:
        return f"Chat: {message} (LLM chưa cấu hình)"

    async def close(self):
        pass