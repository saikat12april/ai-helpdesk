import os
import shutil
from fastapi import APIRouter, UploadFile, File
from backend.services.ocr_service import analyze_screenshot
from backend.services.chat_service import ask_llm # Added for completeness
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    use_knowledge_base: bool = False

@router.post("/ask")
def ask(req: ChatRequest):
    # If use_knowledge_base is True, add your search logic here
    answer = ask_llm(req.message)
    return {"answer": answer}

@router.post("/analyze-screenshot")
async def analyze_image(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        result = analyze_screenshot(file_path)
        return result
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)