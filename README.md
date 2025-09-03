# HR Resource Query Chatbot

An AI-powered HR assistant that answers natural-language queries to find suitable employees based on skills, experience, domain/project background, and availability.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Search/Embeddings**: `sentence-transformers` (all-MiniLM-L6-v2) + FAISS (cosine similarity)
- **Frontend**: Streamlit (simple chat UI)
- **Data**: JSON dataset (15+ realistic employee profiles)

## Features

- Natural language search across employees using embeddings (semantic search)
- REST API:
  - `POST /chat` — ask a natural language question and get recommended candidates
  - `GET /employees/search` — filter employees via query params (skill, project, availability, min_years)
- Streamlit chat UI to interact with the backend visually
- Simple, clean code architecture (RAG-style: Retrieval + light Generation)

## Architecture

```
hr-resource-chatbot/
│── README.md
│── requirements.txt
│── dataset/
│   └── employees.json
│── backend/
│   │── main.py
│   │── models.py
│   │── database.py
│   │── search.py
│   │── rag_pipeline.py
│   └── api/
│       └── routes.py
│── frontend/
│   └── app.py
│── utils/
│   └── __init__.py
│── tests/
│   └── test_api_smoke.py
└── demo/
    └── screenshots/
```

### RAG-ish flow

1. **Retrieval**: Embed employees + query, use FAISS cosine similarity to find relevant profiles
2. **Augmentation**: Combine query intent (skills/domain/exp) with top-k candidates
3. **Generation**: Produce a concise human-readable answer with rationale + list

## Setup & Installation

> Requires Python 3.10+

```bash
cd hr-resource-chatbot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the API

```bash
uvicorn backend.main:app --reload --port 8000
```

- Open API docs: http://localhost:8000/docs

### Run the Streamlit UI

Open a new terminal in the project root:

```bash
streamlit run frontend/app.py
```

- The app defaults to talking to `http://localhost:8000`

## API Documentation

### `POST /chat`

Request body:

```json
{
  "query": "Find Python developers with 3+ years experience who worked on healthcare"
}
```

Response:

```json
{
  "response": "Found 2 candidates...",
  "candidates": [
    {
      "id": 3,
      "name": "John Doe",
      "skills": ["Python", "TensorFlow", "AWS"],
      "experience_years": 4,
      "projects": ["Medical Diagnosis Platform"],
      "availability": "available"
    }
  ]
}
```

### `GET /employees/search`

Query params: `skill`, `project`, `availability`, `min_years`

Example:

```
/employees/search?skill=Python&availability=available&min_years=3
```

## AI Development Process

- Assistant tools used: ChatGPT for architecture scaffolding and boilerplate code generation.
- Usage: Initial repository structure, endpoint stubs, FAISS integration, Streamlit UI wiring.
- Split: ~60% AI-assisted scaffolding, ~40% hand-tuning/testing.
- Challenges: Keeping dependencies compact and avoiding heavy frameworks.

## Technical Decisions

- **Embeddings**: `all-MiniLM-L6-v2` chosen for small size + good semantic performance.
- **Vector store**: FAISS (cosine) for fast top-k retrieval.
- **No external LLM**: The generation step is template-based to remain offline-friendly.
- **FastAPI** preferred for type-safe models and docs.

## Future Improvements

- Add hybrid retrieval: BM25 + embeddings.
- Add optional OpenAI or local LLM for richer response generation.
- Add authentication and per-user history.
- Add persistent FAISS index and incremental updates.

## Demo

- Start both API and Streamlit, then ask:
  - "Find Python developers with 3+ years experience"
  - "Who has worked on healthcare projects?"
  - "Suggest people for a React Native project"
  - "Find developers who know both AWS and Docker"
