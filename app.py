# app.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from qa_engine import get_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HSC Bangla Bot",
    description="Simple RAG QA Bot for Bangla HSC Questions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    response = get_answer(request.query)
    return response
