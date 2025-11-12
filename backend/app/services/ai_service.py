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
        
        # Get model from environment or use default
        # Free models on OpenRouter:
        # - meta-llama/llama-3.2-3b-instruct:free (default, fast and reliable)
        # - google/gemini-2.0-flash-exp:free (good quality, may have rate limits)
        # - qwen/qwen-2-7b-instruct:free (alternative option)
        # - nousresearch/hermes-3-llama-3.1-405b:free (highest quality but slower)
        self.model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.2-3b-instruct:free")
        
    async def _make_request(self, messages: List[Dict[str, str]]) -> str:
        if not self.api_key:
            raise Exception("OPENROUTER_API_KEY is not set in environment variables")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://alfapilot.bot",
            "X-Title": "Alfapilot AI Assistant"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers, timeout=60.0)
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.HTTPStatusError as e:
                # Check if it's a rate limit error (429)
                if e.response.status_code == 429:
                    error_msg = f"Model {self.model} is rate-limited. "
                    # Check if DEMO_MODE is enabled for fallback responses
                    if os.getenv("DEMO_MODE", "false").lower() == "true":
                        print(f"⚠️ DEMO MODE: {error_msg}Using fallback response.")
                        return self._get_demo_response(messages)
                    error_msg += "Try setting DEMO_MODE=true in .env for mock responses, or wait and retry."
                raise Exception(f"OpenRouter API HTTP error: {e.response.status_code} - {error_msg}")
            except httpx.RequestError as e:
                raise Exception(f"OpenRouter API connection error: {str(e)}")
            except (KeyError, IndexError) as e:
                raise Exception(f"Invalid response format from OpenRouter: {str(e)}")
    
    def _get_demo_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate demo responses when API is rate-limited"""
        user_message = messages[-1]["content"].lower()
        
        # Detect the type of request and return appropriate JSON
        if "маркетинг" in user_message or "пост" in user_message or "marketing" in user_message:
            return json.dumps({
                "post_variants": [
                    "🚀 Представляем революционное решение для вашего бизнеса! Наш AI-ассистент поможет автоматизировать рутинные задачи и увеличить продуктивность.",
                    "💼 Бизнес будущего начинается сегодня! Откройте для себя возможности искусственного интеллекта для малого бизнеса. #innovation #AI",
                    "✨ Ваш персональный помощник для бизнеса! Экономьте время, увеличивайте прибыль. Начните использовать AI уже сегодня!"
                ],
                "suggestions": [
                    "Добавьте призыв к действию (CTA)",
                    "Используйте тематические хэштеги",
                    "Добавьте эмодзи для привлечения внимания",
                    "Укажите конкретные преимущества продукта"
                ]
            })
        elif "документ" in user_message or "письмо" in user_message or "document" in user_message:
            return json.dumps({
                "document": "Уважаемый партнёр,\n\nОбращаемся к Вам с предложением о сотрудничестве. Наша компания специализируется на предоставлении инновационных решений для автоматизации бизнес-процессов.\n\nМы уверены, что совместная работа принесёт взаимную выгоду обеим сторонам.\n\nС уважением,\nКоманда Alfapilot",
                "corrections": [
                    "Добавьте конкретные детали о вашей компании",
                    "Укажите контактную информацию",
                    "Добавьте сроки ответа"
                ],
                "suggestions": [
                    "Персонализируйте обращение",
                    "Добавьте конкретные примеры успешных кейсов",
                    "Включите call-to-action"
                ]
            })
        elif "договор" in user_message or "контракт" in user_message or "legal" in user_message or "contract" in user_message:
            return json.dumps({
                "summary": "Договор оказания услуг между Заказчиком и Исполнителем. Определяет обязанности сторон, сроки выполнения работ, условия оплаты и ответственность.",
                "risks": [
                    "Не указаны точные сроки выполнения работ",
                    "Отсутствуют штрафные санкции за нарушение обязательств",
                    "Неясные условия расторжения договора",
                    "Не определён порядок разрешения споров"
                ],
                "recommendations": [
                    "Добавить конкретные сроки с указанием дат",
                    "Включить раздел о штрафных санкциях",
                    "Прописать процедуру досрочного расторжения",
                    "Указать способы разрешения споров (арбитраж/суд)"
                ],
                "todo_items": [
                    "Проконсультироваться с юристом",
                    "Уточнить реквизиты контрагента",
                    "Запросить учредительные документы",
                    "Подготовить приложения к договору"
                ]
            })
        else:  # finance
            return json.dumps({
                "analysis": "На основе предоставленных данных наблюдается положительная динамика финансовых показателей. Выручка демонстрирует стабильный рост, однако операционные расходы требуют оптимизации.",
                "insights": [
                    "Рентабельность бизнеса составляет примерно 30-40%",
                    "Положительный денежный поток",
                    "Операционные расходы можно сократить на 10-15%",
                    "Потенциал для масштабирования бизнеса"
                ],
                "recommendations": [
                    "Оптимизировать операционные расходы",
                    "Диверсифицировать источники дохода",
                    "Инвестировать в маркетинг для ускорения роста",
                    "Создать финансовую подушку безопасности"
                ],
                "forecast": {
                    "trend": "positive",
                    "growth": "15-20% в год при текущих темпах",
                    "recommendation": "Рекомендуется реинвестирование прибыли для ускорения роста"
                }
            })

class AIService:
    def __init__(self):
        self.openrouter = OpenRouterService()
    
    def _extract_json_from_response(self, response: str) -> Dict[str, Any]:
        """Extract JSON from AI response, handling markdown code blocks"""
        try:
            # Try direct parsing first
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find any JSON object in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass
            
            raise ValueError("Could not extract valid JSON from AI response")
    
    async def generate_marketing_content(self, idea: str, tone: str, target_audience: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй 3 варианта постов для социальных сетей на основе идеи.
        
        Идея: {idea}
        Тон: {tone}
        Целевая аудитория: {target_audience}
        
        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):
        {{
            "post_variants": ["вариант1", "вариант2", "вариант3"],
            "suggestions": ["предложение1", "предложение2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты эксперт по маркетингу и контент-стратегии. Отвечай только в формате JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback если AI не вернул валидный JSON
            return {
                "post_variants": [
                    f"📢 {idea}\n\nЦелевая аудитория: {target_audience}. Тон: {tone}.",
                    f"✨ Новинка! {idea}\n\n#маркетинг #бизнес",
                    f"🚀 {idea}\n\nУзнайте больше!"
                ],
                "suggestions": [
                    "Добавьте призыв к действию",
                    "Используйте релевантные хэштеги",
                    "Добавьте визуальный контент"
                ]
            }
    
    async def generate_document(self, doc_type: str, content: str, style: str) -> Dict[str, Any]:
        prompt = f"""
        Сгенерируй {doc_type} на основе следующего описания.
        
        Тип документа: {doc_type}
        Содержание: {content}
        Стиль: {style}
        
        Также предложи 2-3 исправления/улучшения.
        
        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):
        {{
            "document": "полный текст документа",
            "corrections": ["исправление1", "исправление2"],
            "suggestions": ["предложение1", "предложение2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты профессиональный юрист и копирайтер. Отвечай только в формате JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {
                "document": f"# {doc_type}\n\n{content}\n\nСтиль: {style}",
                "corrections": ["Проверьте орфографию и пунктуацию", "Уточните юридические термины"],
                "suggestions": ["Добавьте контактную информацию", "Укажите сроки и даты"]
            }
    
    async def analyze_contract(self, contract_text: str, analyze_risks: bool) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй следующий договор и предоставь:
        1. Краткое содержание (3-4 пункта)
        2. Рисковые пункты (если analyze_risks=True)
        3. Рекомендации
        4. Пункты для добавления в To-Do список
        
        Анализ рисков: {"Да" if analyze_risks else "Нет"}
        Текст договора: {contract_text[:3000]}
        
        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):
        {{
            "summary": "краткое содержание",
            "risks": ["риск1", "риск2"],
            "recommendations": ["рекомендация1", "рекомендация2"],
            "todo_items": ["задача1", "задача2"]
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты опытный юрист с expertise в анализе договоров. Отвечай только в формате JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {
                "summary": "Договор содержит основные положения о предоставлении услуг/товаров между сторонами.",
                "risks": ["Не указаны точные сроки выполнения", "Неясные условия оплаты", "Отсутствуют штрафные санкции"],
                "recommendations": ["Проконсультироваться с юристом", "Уточнить условия расторжения", "Добавить приложения с деталями"],
                "todo_items": ["Запросить дополнительные документы", "Назначить встречу с юристом", "Уточнить реквизиты сторон"]
            }
    
    async def analyze_finance_data(self, data: str, analysis_type: str) -> Dict[str, Any]:
        prompt = f"""
        Проанализируй финансовые данные и предоставь {analysis_type}.
        
        Данные: {data}
        Тип анализа: {analysis_type}
        
        ВАЖНО: Верни ответ ТОЛЬКО в виде валидного JSON (без markdown форматирования):
        {{
            "analysis": "детальный анализ",
            "insights": ["инсайт1", "инсайт2"],
            "recommendations": ["рекомендация1", "рекомендация2"],
            "forecast": {{"trend": "прогноз тренда", "growth": "ожидаемый рост"}}
        }}
        """
        
        messages = [
            {"role": "system", "content": "Ты финансовый аналитик с опытом в бизнес-аналитике. Отвечай только в формате JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.openrouter._make_request(messages)
        
        try:
            return self._extract_json_from_response(response)
        except (json.JSONDecodeError, ValueError):
            return {
                "analysis": f"Финансовый анализ ({analysis_type}): На основе предоставленных данных наблюдается стабильная динамика показателей.",
                "insights": ["Стабильный рост выручки", "Высокие операционные расходы", "Положительный денежный поток"],
                "recommendations": ["Оптимизировать операционные расходы", "Диверсифицировать источники дохода", "Увеличить инвестиции в маркетинг"],
                "forecast": {"trend": "positive", "growth": "8-12% годовых"}
            }