from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI(title="HR Resource Query Chatbot", version="1.0.0")

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "HR Chatbot API is running"}
