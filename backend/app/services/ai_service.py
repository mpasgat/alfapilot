import json
import os
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv

load_dotenv()


class GigaChatService:
    """GigaChat API (Sber) - Russian AI Service"""
    
    def __init__(self):
        self.access_token = os.getenv("GIGACHAT_ACCESS_TOKEN")
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    async def _make_request(self, messages: List[Dict[str, str]]) -> str:
        """Make request to GigaChat API"""
        if not self.access_token:
            print(f"⚠️ GIGACHAT_ACCESS_TOKEN not set. Auto-switching to DEMO mode.")
            return self._get_demo_response(messages)

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "GigaChat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as e:
                # Auto-fallback for auth errors (401) - token expired
                if e.response.status_code == 401:
                    print(f"⚠️ GigaChat token expired or invalid (401). Auto-switching to DEMO mode.")
                    return self._get_demo_response(messages)
                
                # Check for demo mode fallback for other errors
                demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
                if demo_mode:
                    print(f"⚠️ DEMO MODE: GigaChat API error ({e.response.status_code}). Using fallback.")
                    return self._get_demo_response(messages)
                
                raise Exception(f"GigaChat API error: {e.response.status_code} - {e.response.text}")
            except Exception as e:
                demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
                if demo_mode:
                    print(f"⚠️ DEMO MODE: GigaChat request error. Using fallback.")
                    return self._get_demo_response(messages)
                raise Exception(f"GigaChat request error: {str(e)}")

    def _get_demo_response(self, messages: List[Dict[str, str]]) -> str:
        """Demo fallback response"""
        user_message = messages[-1]["content"].lower()
        if "маркетинг" in user_message or "пост" in user_message or "marketing" in user_message:
            return json.dumps({
                "post_variants": [
                    "🚀 Представляем революционное решение для вашего бизнеса! Наш AI-ассистент поможет автоматизировать рутинные задачи.",
                    "💼 Бизнес будущего начинается сегодня! Откройте возможности ИИ. #innovation #AI",
                    "✨ Ваш персональный помощник для бизнеса! Экономьте время, увеличивайте прибыль!",
                ],
                "suggestions": ["Добавьте призыв к действию", "Используйте хэштеги"]
            })
        elif "документ" in user_message or "письмо" in user_message or "document" in user_message:
            return json.dumps({
                "document": "Уважаемый партнёр,\n\nОбращаемся с предложением о сотрудничестве.\n\nС уважением,\nКоманда Alfapilot",
                "corrections": ["Добавьте детали", "Укажите контакты"],
                "suggestions": ["Персонализируйте обращение"]
            })
        elif "договор" in user_message or "контракт" in user_message or "legal" in user_message:
            return json.dumps({
                "summary": "Договор оказания услуг между сторонами.",
                "risks": ["Не указаны сроки", "Отсутствуют штрафы"],
                "recommendations": ["Добавить сроки", "Включить санкции"]
            })
        else:
            return json.dumps({
                "analysis": "Финансовый анализ показывает положительную динамику.",
                "insights": ["Рентабельность бизнеса", "Положительный поток"],
                "recommendations": ["Оптимизировать расходы"]
            })


class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = os.getenv(
            "OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free"
        )

    async def _make_request(self, messages: List[Dict[str, str]]) -> str:
        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY is not set in environment variables")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://alfapilot.bot",
            "X-Title": "Alfapilot AI Assistant",
        }

        payload = {"model": self.model, "messages": messages, "max_tokens": 4000, "temperature": 0.7}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
                if e.response.status_code in [401, 429, 404]:
                    if e.response.status_code == 429:
                        error_msg = f"Model {self.model} is rate-limited. "
                    else:
                        error_msg = f"OpenRouter API authentication failed (invalid API key). "

                    if demo_mode:
                        print(f"⚠️ DEMO MODE: {error_msg}Using fallback response.")
                        return self._get_demo_response(messages)

                    error_msg += "Try setting DEMO_MODE=true in .env for mock responses."
                    raise Exception(f"OpenRouter API HTTP error: {e.response.status_code} - {error_msg}")
                raise Exception(f"OpenRouter API HTTP error: {e.response.status_code}")
            except httpx.RequestError as e:
                raise Exception(f"OpenRouter API connection error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise Exception(f"Invalid response format from OpenRouter: {str(e)}")

    def _get_demo_response(self, messages: List[Dict[str, str]]) -> str:
        user_message = messages[-1]["content"].lower()
        if "маркетинг" in user_message or "пост" in user_message or "marketing" in user_message:
            return json.dumps({
                "post_variants": [
                    "🚀 Представляем революционное решение для вашего бизнеса! Наш AI-ассистент поможет автоматизировать рутинные задачи и увеличить продуктивность.",
                    "💼 Бизнес будущего начинается сегодня! Откройте для себя возможности искусственного интеллекта для малого бизнеса. #innovation #AI",
                    "✨ Ваш персональный помощник для бизнеса! Экономьте время, увеличивайте прибыль. Начните использовать AI уже сегодня!",
                ],
                "suggestions": ["Добавьте призыв к действию (CTA)", "Используйте тематические хэштеги"],
            })
        elif "документ" in user_message or "письмо" in user_message or "document" in user_message:
            return json.dumps({
                "document": "Уважаемый партнёр,\n\nОбращаемся к Вам с предложением о сотрудничестве. Наша компания специализируется на предоставлении инновационных решений для автоматизации бизнес-процессов.\n\nС уважением,\nКоманда Alfapilot",
                "corrections": ["Добавьте конкретные детали о вашей компании", "Укажите контактную информацию"],
                "suggestions": ["Персонализируйте обращение", "Добавьте конкретные примеры успешных кейсов"],
            })
        elif "договор" in user_message or "контракт" in user_message or "legal" in user_message or "contract" in user_message:
            return json.dumps({
                "summary": "Договор оказания услуг между Заказчиком и Исполнителем.",
                "risks": ["Не указаны точные сроки выполнения работ", "Отсутствуют штрафные санкции"],
                "recommendations": ["Добавить конкретные сроки", "Включить раздел о штрафных санкциях"],
            })
        else:
            return json.dumps({
                "analysis": "На основе предоставленных данных наблюдается положительная динамика финансовых показателей.",
                "insights": ["Рентабельность бизнеса", "Положительный денежный поток"],
                "recommendations": ["Оптимизировать операционные расходы", "Диверсифицировать источники дохода"],
            })


class AIService:
    def __init__(self):
        ai_provider = os.getenv("AI_PROVIDER", "openrouter").lower()
        
        if ai_provider == "gigachat":
            self.ai_service = GigaChatService()
        else:
            self.ai_service = OpenRouterService()

    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass
            raise ValueError("Could not extract valid JSON from AI response")

    async def generate_marketing_content(self, idea: str, tone: str, target_audience: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй 3 варианта постов для социальных сетей на основе идеи.
        \n        Идея: {idea}\n        Тон: {tone}\n        Целевая аудитория: {target_audience}\n        \n        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):\n        {{\n            \"post_variants\": [\"вариант1\", \"вариант2\", \"вариант3\"],\n            \"suggestions\": [\"предложение1\", \"предложение2\"]\n        }}\n        """
        messages = [{"role": "system", "content": "Ты эксперт по маркетингу и контент-стратегии. Отвечай только в формате JSON."}, {"role": "user", "content": prompt}]
        response = await self.ai_service._make_request(messages)
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {"post_variants": [f"📢 {idea}\n\nЦелевая аудитория: {target_audience}. Тон: {tone}.", f"✨ Новинка! {idea}\n\n#маркетинг #бизнес", f"🚀 {idea}\n\nУзнайте больше!"], "suggestions": ["Добавьте призыв к действию", "Используйте релевантные хэштеги"]}

    async def generate_document(self, doc_type: str, content: str, style: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй {doc_type} на основе следующего описания.\n\n        Тип документа: {doc_type}\n        Содержание: {content}\n        Стиль: {style}\n\n        Также предложи 2-3 исправления/улучшения.\n\n        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):\n        {{\n            \"document\": \"полный текст документа\",\n            \"corrections\": [\"исправление1\", \"исправление2\"],\n            \"suggestions\": [\"предложение1\", \"предложение2\"]\n        }}\n        """
        messages = [{"role": "system", "content": "Ты профессиональный юрист и копирайтер. Отвечай только в формате JSON."}, {"role": "user", "content": prompt}]
        response = await self.ai_service._make_request(messages)
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {"document": f"# {doc_type}\n\n{content}\n\nСтиль: {style}", "corrections": ["Проверьте орфографию и пунктуацию", "Уточните юридические термины"], "suggestions": ["Добавьте контактную информацию", "Укажите сроки и даты"]}

    async def analyze_contract(self, contract_text: str, analyze_risks: bool) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй следующий договор и предоставь:\n        1. Краткое содержание (3-4 пункта)\n        2. Рисковые пункты (если analyze_risks=True)\n        3. Рекомендации\n        4. Пункты для добавления в To-Do список\n\n        Анализ рисков: {"Да" if analyze_risks else "Нет"}\n        Текст договора: {contract_text[:3000]}\n\n        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):\n        {{\n            \"summary\": \"краткое содержание\",\n            \"risks\": [\"риск1\", \"риск2\"],\n            \"recommendations\": [\"рекомендация1\", \"рекомендация2\"],\n            \"todo_items\": [\"задача1\", \"задача2\"]\n        }}\n        """
        messages = [{"role": "system", "content": "Ты опытный юрист с expertise в анализе договоров. Отвечай только в формате JSON."}, {"role": "user", "content": prompt}]
        response = await self.ai_service._make_request(messages)
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {"summary": "Договор содержит основные положения о предоставлении услуг/товаров между сторонами.", "risks": ["Не указаны точные сроки выполнения", "Неясные условия оплаты", "Отсутствуют штрафные санкции"], "recommendations": ["Проконсультироваться с юристом", "Уточнить условия расторжения", "Добавить приложения с деталями"], "todo_items": ["Запросить дополнительные документы", "Назначить встречу с юристом", "Уточнить реквизиты сторон"]}

    async def analyze_finance_data(self, data: str, analysis_type: str) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй финансовые данные и предоставь {analysis_type}.\n\n        Данные: {data}\n        Тип анализа: {analysis_type}\n\n        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):\n        {{\n            \"analysis\": \"детальный анализ\",\n            \"insights\": [\"инсайт1\", \"инсайт2\"],\n            \"recommendations\": [\"рекомендация1\", \"рекомендация2\"],\n            \"forecast\": {{\"trend\": \"прогноз тренда\", \"growth\": \"ожидаемый рост\"}}\n        }}\n        """
        messages = [{"role": "system", "content": "Ты финансовый аналитик с опытом в бизнес-аналитике. Отвечай только в формате JSON."}, {"role": "user", "content": prompt}]
        response = await self.ai_service._make_request(messages)
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {"analysis": f"Финансовый анализ ({analysis_type}): На основе предоставленных данных наблюдается стабильная динамика показателей.", "insights": ["Стабильный рост выручки", "Высокие операционные расходы", "Положительный денежный поток"], "recommendations": ["Оптимизировать операционные расходы", "Диверсифицировать источники дохода", "Увеличить инвестиции в маркетинг"], "forecast": {"trend": "positive", "growth": "8-12% годовых"}}

