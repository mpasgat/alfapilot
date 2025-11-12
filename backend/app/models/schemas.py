from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MarketingRequest(BaseModel):
    idea: str
    tone: Optional[str] = "professional"
    target_audience: Optional[str] = "general"

class MarketingResponse(BaseModel):
    post_variants: List[str]
    suggestions: List[str]

class DocumentRequest(BaseModel):
    doc_type: str
    content: str
    style: Optional[str] = "formal"

class DocumentResponse(BaseModel):
    document: str
    corrections: List[str]
    suggestions: List[str]

class LegalAnalysisRequest(BaseModel):
    contract_text: str
    analyze_risks: bool = True

class LegalAnalysisResponse(BaseModel):
    summary: str
    risks: List[str]
    recommendations: List[str]
    todo_items: List[str]

class FinanceAnalysisRequest(BaseModel):
    data: str
    analysis_type: str  # "comparison", "forecast", "summary"

class FinanceAnalysisResponse(BaseModel):
    analysis: str
    insights: List[str]
    recommendations: List[str]
    forecast: Optional[Dict[str, Any]] = None

class AIErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None