from typing import List
from .database import load_employees
from .search import semantic_search
from .models import ChatResponse, Employee

def _summarize(cands: List[Employee], query: str) -> str:
    if not cands:
        return f"I couldn't find matching candidates for: '{query}'. Try adjusting skills or experience keywords."
    intro = f"Based on your query — {query} — I found {len(cands)} candidate(s). Here are the best matches:"
    lines = []
    for e in cands:
        lines.append(f"- {e.name} ({e.experience_years} yrs): Skills={', '.join(e.skills)}; Projects={', '.join(e.projects)}; Availability={e.availability}")
    outro = "Would you like me to filter by availability, minimum years, or a specific tech stack?"
    return "\n".join([intro, *lines, outro])

def handle_query(query: str, top_k: int = 5) -> ChatResponse:
    employees = load_employees()
    matched = semantic_search(query, employees, top_k=top_k)
    response_text = _summarize(matched, query)
    return ChatResponse(response=response_text, candidates=matched)
