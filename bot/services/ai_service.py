import os
from typing import Any, Dict, List

import httpx


class BackendService:
    def __init__(self):
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

    async def _make_request(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Универсальный метод для запросов к бэкенду"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self.backend_url}{endpoint}", json=data)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            raise Exception(f"Backend request error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    async def generate_marketing_posts(
        self, idea: str, tone: str = "professional", target_audience: str = "general"
    ) -> Dict[str, Any]:
        """Генерация постов через бэкенд"""
        return await self._make_request(
            "/api/v1/marketing/generate-posts",
            {"idea": idea, "tone": tone, "target_audience": target_audience},
        )

    async def generate_stories(self, idea: str) -> Dict[str, Any]:
        """Генерация сторис через бэкенд"""
        return await self._make_request(
            "/api/v1/marketing/generate-stories", {"idea": idea}
        )

    async def generate_document(
        self, doc_type: str, content: str, style: str = "formal"
    ) -> Dict[str, Any]:
        """Генерация документов через бэкенд"""
        return await self._make_request(
            "/api/v1/documents/generate-document",
            {"doc_type": doc_type, "content": content, "style": style},
        )

    async def analyze_contract(
        self, contract_text: str, analyze_risks: bool = True
    ) -> Dict[str, Any]:
        """Анализ договора через бэкенд"""
        return await self._make_request(
            "/api/v1/legal/analyze-contract",
            {"contract_text": contract_text, "analyze_risks": analyze_risks},
        )

    async def analyze_finance_data(
        self, data: str, analysis_type: str
    ) -> Dict[str, Any]:
        """Анализ финансовых данных через бэкенд"""
        return await self._make_request(
            "/api/v1/finance/analyze-data",
            {"data": data, "analysis_type": analysis_type},
        )
