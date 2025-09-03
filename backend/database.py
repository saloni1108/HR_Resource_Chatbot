import json
from pathlib import Path
from typing import List
from .models import Employee

DATA_PATH = Path(__file__).resolve().parents[1] / "dataset" / "employees.json"

def load_employees() -> List[Employee]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [Employee(**e) for e in raw]
