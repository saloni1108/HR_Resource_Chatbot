from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .models import Employee

_model = None
_index = None
_emp_vectors = None
_emp_meta: List[Employee] = []

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model

def _employee_to_text(e: Employee) -> str:
    return (
        f"Name: {e.name}. Skills: {', '.join(e.skills)}. "
        f"Experience: {e.experience_years} years. "
        f"Projects: {', '.join(e.projects)}. Availability: {e.availability}."
    )

def _build_index(employees: List[Employee]):
    global _index, _emp_vectors, _emp_meta
    model = _get_model()
    corpus = [_employee_to_text(e) for e in employees]
    emb = model.encode(corpus, normalize_embeddings=True, convert_to_numpy=True)
    dim = emb.shape[1]
    index = faiss.IndexFlatIP(dim) 
    index.add(emb.astype(np.float32))
    _index = index
    _emp_vectors = emb
    _emp_meta = employees

def ensure_index(employees: List[Employee]):
    if _index is None or _emp_meta != employees:
        _build_index(employees)

def semantic_search(query: str, employees: List[Employee], top_k: int = 5) -> List[Employee]:
    ensure_index(employees)
    model = _get_model()
    q = model.encode([query], normalize_embeddings=True, convert_to_numpy=True).astype(np.float32)
    D, I = _index.search(q, top_k)
    idxs = I[0]
    result = []
    for ix in idxs:
        if ix == -1:  # safety
            continue
        result.append(_emp_meta[int(ix)])
    return result
