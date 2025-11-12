from fastapi import APIRouter, HTTPException
from app.models.schemas import LegalAnalysisRequest, LegalAnalysisResponse, AIErrorResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/analyze-contract", response_model=LegalAnalysisResponse, responses={500: {"model": AIErrorResponse}})
async def analyze_contract(request: LegalAnalysisRequest):
    try:
        result = await ai_service.analyze_contract(
            contract_text=request.contract_text,
            analyze_risks=request.analyze_risks
        )
        return LegalAnalysisResponse(
            summary=result.get("summary", ""),
            risks=result.get("risks", []),
            recommendations=result.get("recommendations", []),
            todo_items=result.get("todo_items", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")