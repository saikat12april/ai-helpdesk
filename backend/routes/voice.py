from fastapi import APIRouter
from pydantic import BaseModel
# Assuming you have these implemented in your services:
from backend.services.chat_service import ask_llm
from backend.services.vector_db import search_knowledge

router = APIRouter(prefix="/voice", tags=["Voice Assistant"])

class SpeakRequest(BaseModel):
    text: str

@router.get("/status")
def voice_status():
    return {"voice_ready": True, "message": "Browser Voice APIs active!"}

@router.post("/ask-voice")
def ask_voice(req: SpeakRequest):
    context = search_knowledge(req.text)
    prompt = req.text + " (Provide a concise, conversational answer without complex formatting like bolding or bullet points, as this will be read aloud by a Text-to-Speech engine.)"
    answer = ask_llm(prompt, context)
    return {"question": req.text, "answer": answer}