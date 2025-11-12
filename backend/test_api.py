"""
Test script for Alfapilot FastAPI Backend
Run this after starting the backend server
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    print("\n=== Testing /health endpoint ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        print("✅ Health check passed")

async def test_marketing():
    """Test marketing endpoint"""
    print("\n=== Testing /api/v1/marketing/generate-posts ===")
    payload = {
        "idea": "Запуск нового AI-ассистента для бизнеса",
        "tone": "professional",
        "target_audience": "предприниматели и стартапы"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/marketing/generate-posts",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert "post_variants" in data
        assert "suggestions" in data
        assert len(data["post_variants"]) > 0
        print("✅ Marketing endpoint passed")

async def test_documents():
    """Test documents endpoint"""
    print("\n=== Testing /api/v1/documents/generate-document ===")
    payload = {
        "doc_type": "письмо-запрос",
        "content": "Нужно составить письмо для запроса информации о партнерстве",
        "style": "formal"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/documents/generate-document",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert "document" in data
        assert "corrections" in data
        assert "suggestions" in data
        print("✅ Documents endpoint passed")

async def test_legal():
    """Test legal analysis endpoint"""
    print("\n=== Testing /api/v1/legal/analyze-contract ===")
    payload = {
        "contract_text": """
        ДОГОВОР ОКАЗАНИЯ УСЛУГ №123
        
        Заказчик обязуется оплатить услуги в течение 30 дней.
        Исполнитель обязуется предоставить результаты работы.
        """,
        "analyze_risks": True
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/legal/analyze-contract",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert "summary" in data
        assert "risks" in data
        assert "recommendations" in data
        assert "todo_items" in data
        print("✅ Legal endpoint passed")

async def test_finance():
    """Test finance analysis endpoint"""
    print("\n=== Testing /api/v1/finance/analyze-data ===")
    payload = {
        "data": "Выручка за Q1: 1,000,000 руб, расходы: 700,000 руб",
        "analysis_type": "summary"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/finance/analyze-data",
            json=payload
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        assert response.status_code == 200
        assert "analysis" in data
        assert "insights" in data
        assert "recommendations" in data
        print("✅ Finance endpoint passed")

async def main():
    """Run all tests"""
    print("🚀 Starting API tests...\n")
    
    try:
        await test_health()
        await test_marketing()
        await test_documents()
        await test_legal()
        await test_finance()
        
        print("\n" + "="*50)
        print("✅ All tests passed successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
