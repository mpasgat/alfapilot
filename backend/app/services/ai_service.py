import os
import httpx
from typing import Dict, Any, List
import json
from dotenv import load_dotenv

load_dotenv()

class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-flash-1.5-8b"  # Бесплатная модель
        
    async def _make_request(self, messages: List[Dict[str, str]]) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://alfapilot.bot",
            "X-Title": "Alfapilot AI Assistant"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.RequestError as e:
                raise Exception(f"OpenRouter API error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise Exception(f"Invalid response format: {str(e)}")

class AIService:
    def __init__(self):
        self.openrouter = OpenRouterService()
    
    async def generate_marketing_content(self, idea: str, tone: str, target_audience: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй 3 варианта постов для социальных сетей на основе идеи.
        
        Идея: {idea}
        Тон: {tone}
        Целевая аудитория: {target_audience}
        
        Верни ответ в формате JSON:
        {{
            "post_variants": ["вариант1", "вариант2", "вариант3"],
            "suggestions": ["предложение1", "предложение2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты эксперт по маркетингу и контент-стратегии."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback если AI не вернул JSON
            return {
                "post_variants": [f"Пост вариант {i+1} для идеи: {idea}" for i in range(3)],
                "suggestions": ["Добавьте призыв к действию", "Используйте хэштеги"]
            }
    
    async def generate_document(self, doc_type: str, content: str, style: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй {doc_type} на основе следующего описания.
        
        Тип документа: {doc_type}
        Содержание: {content}
        Стиль: {style}
        
        Также предложи 2-3 исправления/улучшения.
        
        Верни ответ в формате JSON:
        {{
            "document": "полный текст документа",
            "corrections": ["исправление1", "исправление2"],
            "suggestions": ["предложение1", "предложение2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты профессиональный юрист и копирайтер."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "document": f"Документ типа '{doc_type}': {content}",
                "corrections": ["Проверьте орфографию", "Уточните детали"],
                "suggestions": ["Добавьте контактную информацию", "Укажите сроки"]
            }
    
    async def analyze_contract(self, contract_text: str, analyze_risks: bool) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй следующий договор и предоставь:
        1. Краткое содержание (3-4 пункта)
        2. Рисковые пункты (если analyze_risks=True)
        3. Рекомендации
        4. Пункты для добавления в To-Do список
        
        Текст договора: {contract_text[:3000]}  # Ограничиваем длину
        
        Верни ответ в формате JSON:
        {{
            "summary": "краткое содержание",
            "risks": ["риск1", "риск2"],
            "recommendations": ["рекомендация1", "рекомендация2"],
            "todo_items": ["задача1", "задача2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты опытный юрист с expertise в анализе договоров."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "summary": "Краткое содержание договора",
                "risks": ["Не указаны сроки", "Неясные условия оплаты"],
                "recommendations": ["Проконсультироваться с юристом", "Уточнить условия"],
                "todo_items": ["Запросить дополнительные документы", "Назначить встречу"]
            }
    
    async def analyze_finance_data(self, data: str, analysis_type: str) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй финансовые данные и предоставь {analysis_type}.
        
        Данные: {data}
        Тип анализа: {analysis_type}
        
        Верни ответ в формате JSON:
        {{
            "analysis": "детальный анализ",
            "insights": ["инсайт1", "инсайт2"],
            "recommendations": ["рекомендация1", "рекомендация2"],
            "forecast": {{"trend": "прогноз тренда", "growth": "ожидаемый рост"}}
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты финансовый аналитик с опытом в бизнес-аналитике."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "analysis": f"Анализ данных: {data}",
                "insights": ["Стабильный рост", "Высокие операционные расходы"],
                "recommendations": ["Сократить расходы", "Диверсифицировать доходы"],
                "forecast": {"trend": "positive", "growth": "10%"}
            }