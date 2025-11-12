"""
Example: How to integrate the bot with the backend API
This shows how your bot can call the backend endpoints
"""

import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

async def call_marketing_api(idea: str, tone: str = "professional", target_audience: str = "general"):
    """Call marketing endpoint to generate social media posts"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/marketing/generate-posts",
                json={
                    "idea": idea,
                    "tone": tone,
                    "target_audience": target_audience
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"API Error: {str(e)}"}

async def call_documents_api(doc_type: str, content: str, style: str = "formal"):
    """Call documents endpoint to generate documents"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/documents/generate-document",
                json={
                    "doc_type": doc_type,
                    "content": content,
                    "style": style
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"API Error: {str(e)}"}

async def call_legal_api(contract_text: str, analyze_risks: bool = True):
    """Call legal endpoint to analyze contracts"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/legal/analyze-contract",
                json={
                    "contract_text": contract_text,
                    "analyze_risks": analyze_risks
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"API Error: {str(e)}"}

async def call_finance_api(data: str, analysis_type: str = "summary"):
    """Call finance endpoint to analyze financial data"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{BACKEND_URL}/api/v1/finance/analyze-data",
                json={
                    "data": data,
                    "analysis_type": analysis_type
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"API Error: {str(e)}"}

# Example usage in your bot handlers
async def example_usage():
    """Example of how to use these functions in your bot"""
    
    # Example 1: Marketing
    print("\n=== Marketing Example ===")
    result = await call_marketing_api(
        idea="Запуск нового AI-ассистента для малого бизнеса",
        tone="friendly",
        target_audience="владельцы малого бизнеса"
    )
    if "error" not in result:
        print("✅ Post variants generated:")
        for i, post in enumerate(result.get("post_variants", []), 1):
            print(f"\n{i}. {post}")
        print(f"\n💡 Suggestions: {', '.join(result.get('suggestions', []))}")
    else:
        print(f"❌ {result['error']}")
    
    # Example 2: Documents
    print("\n=== Documents Example ===")
    result = await call_documents_api(
        doc_type="деловое письмо",
        content="Нужно составить письмо партнеру с предложением о сотрудничестве",
        style="formal"
    )
    if "error" not in result:
        print("✅ Document generated:")
        print(result.get("document", "")[:200] + "...")
        print(f"\n💡 Suggestions: {', '.join(result.get('suggestions', []))}")
    else:
        print(f"❌ {result['error']}")
    
    # Example 3: Legal
    print("\n=== Legal Example ===")
    result = await call_legal_api(
        contract_text="Договор оказания услуг между Заказчиком и Исполнителем...",
        analyze_risks=True
    )
    if "error" not in result:
        print("✅ Contract analyzed:")
        print(f"Summary: {result.get('summary', '')}")
        print(f"⚠️ Risks: {', '.join(result.get('risks', []))}")
        print(f"📋 Todo: {', '.join(result.get('todo_items', []))}")
    else:
        print(f"❌ {result['error']}")
    
    # Example 4: Finance
    print("\n=== Finance Example ===")
    result = await call_finance_api(
        data="Выручка за Q1: 1,500,000 руб, Расходы: 900,000 руб",
        analysis_type="summary"
    )
    if "error" not in result:
        print("✅ Finance analysis:")
        print(f"Analysis: {result.get('analysis', '')[:200]}...")
        print(f"💡 Insights: {', '.join(result.get('insights', []))}")
    else:
        print(f"❌ {result['error']}")

if __name__ == "__main__":
    print("🤖 Testing Bot-Backend Integration\n")
    asyncio.run(example_usage())
