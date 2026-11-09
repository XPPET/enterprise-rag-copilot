from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_engine import query_copilot, EnterpriseResponse

app = FastAPI(
    title="Enterprise AI Copilot",
    description="RAG Engine for Corporate Document Intelligence & Risk Analysis",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/v1/query", response_model=EnterpriseResponse)
def execute_query(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Το ερώτημα δεν μπορεί να είναι κενό.")
    
    try:
        result = query_copilot(payload.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Enterprise AI Copilot"}