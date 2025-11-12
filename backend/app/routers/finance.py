from fastapi import APIRouter, HTTPException
from app.models.schemas import FinanceAnalysisRequest, FinanceAnalysisResponse, AIErrorResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/analyze-data", response_model=FinanceAnalysisResponse, responses={500: {"model": AIErrorResponse}})
async def analyze_finance_data(request: FinanceAnalysisRequest):
    try:
        result = await ai_service.analyze_finance_data(
            data=request.data,
            analysis_type=request.analysis_type
        )
        return FinanceAnalysisResponse(
            analysis=result.get("analysis", ""),
            insights=result.get("insights", []),
            recommendations=result.get("recommendations", []),
            forecast=result.get("forecast", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")