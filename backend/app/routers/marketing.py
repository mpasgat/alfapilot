from fastapi import APIRouter, HTTPException
from app.models.schemas import MarketingRequest, MarketingResponse, AIErrorResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/generate-posts", response_model=MarketingResponse, responses={500: {"model": AIErrorResponse}})
async def generate_marketing_posts(request: MarketingRequest):
    try:
        result = await ai_service.generate_marketing_content(
            idea=request.idea,
            tone=request.tone,
            target_audience=request.target_audience
        )
        return MarketingResponse(
            post_variants=result.get("post_variants", []),
            suggestions=result.get("suggestions", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@router.post("/generate-stories")
async def generate_stories(idea: str):
    try:
        # TODO: Реализовать генерацию сторис
        return {"stories": ["Сторис вариант 1", "Сторис вариант 2"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))