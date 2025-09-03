from fastapi import APIRouter, Query
from typing import Optional, List
from ..models import QueryRequest, ChatResponse, Employee
from ..rag_pipeline import handle_query
from ..database import load_employees

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: QueryRequest) -> ChatResponse:
    return handle_query(req.query, top_k=req.top_k or 5)

@router.get("/employees/search", response_model=List[Employee])
async def search_employees(
    skill: Optional[str] = Query(None),
    project: Optional[str] = Query(None),
    availability: Optional[str] = Query(None),
    min_years: Optional[int] = Query(None, ge=0),
):
    employees = load_employees()
    def ok(e: Employee) -> bool:
        if skill and skill not in e.skills:
            return False
        if project and project not in e.projects:
            return False
        if availability and e.availability != availability:
            return False
        if min_years is not None and e.experience_years < min_years:
            return False
        return True
    return [e for e in employees if ok(e)]
