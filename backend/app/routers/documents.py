from fastapi import APIRouter, HTTPException
from app.models.schemas import DocumentRequest, DocumentResponse, AIErrorResponse
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/generate-document", response_model=DocumentResponse, responses={500: {"model": AIErrorResponse}})
async def generate_document(request: DocumentRequest):
    try:
        result = await ai_service.generate_document(
            doc_type=request.doc_type,
            content=request.content,
            style=request.style
        )
        return DocumentResponse(
            document=result.get("document", ""),
            corrections=result.get("corrections", []),
            suggestions=result.get("suggestions", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")