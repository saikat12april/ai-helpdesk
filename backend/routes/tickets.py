from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from mongoengine import Document, StringField, DateTimeField
# Removed SequenceField
from backend.services.chat_service import ask_llm

router = APIRouter(prefix="/tickets", tags=["Tickets"])

# ─── DATABASE MODEL ───
class Ticket(Document):
    # Removed id = SequenceField(...), letting MongoDB handle _id natively
    title = StringField(required=True)
    description = StringField(required=True)
    category = StringField(default="General")
    department = StringField(default="General")
    priority = StringField(default="Medium")
    status = StringField(default="Open")
    ai_suggested_fix = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'tickets'}

# ─── SCHEMAS ───
class TicketReq(BaseModel):
    title: str
    description: str
    category: str
    department: str
    priority: Optional[str] = None

# ─── ROUTES ───
@router.post("/create")
def create_ticket(req: TicketReq):
    priority = req.priority
    fix = ""
    
    # AI Auto-Triage if no priority is set
    if not priority:
        prompt = f"Analyze this IT issue: '{req.title} - {req.description}'. Reply ONLY with the priority level (Critical, High, Medium, Low) on line 1, and a short 2-step suggested fix on line 2."
        ai_resp = ask_llm(prompt)
        parts = ai_resp.split('\n', 1)
        
        detected = parts[0].strip().title()
        priority = detected if detected in ["Critical", "High", "Medium", "Low"] else "Medium"
        fix = parts[1].strip() if len(parts) > 1 else "No automatic fix available."

    t = Ticket(
        title=req.title, description=req.description, category=req.category,
        department=req.department, priority=priority, ai_suggested_fix=fix
    ).save()
    
    # Return string representation of the native MongoDB ObjectId
    return {"message": "Ticket created", "ticket_id": str(t.id), "priority": priority, "ai_suggested_fix": fix}

@router.get("/all")
def get_tickets(status: str = None, priority: str = None):
    query = {}
    if status and status != "All": query["status"] = status
    if priority and priority != "All": query["priority"] = priority
    
    tickets = Ticket.objects(**query).order_by('-created_at')
    
    # Convert t.id to str to avoid JSON serialization errors
    return [{
        "id": str(t.id), 
        "title": t.title, 
        "description": t.description, 
        "category": t.category, 
        "department": t.department, 
        "priority": t.priority, 
        "status": t.status, 
        "ai_suggested_fix": t.ai_suggested_fix, 
        "created_at": str(t.created_at)
    } for t in tickets]

@router.put("/{ticket_id}/update")
def update_ticket(ticket_id: str, req: dict):
    # ticket_id is now a string to match the ObjectId
    t = Ticket.objects(id=ticket_id).first()
    if t: 
        t.update(set__status=req.get("status", t.status))
        return {"message": "Updated"}
    return {"error": "Ticket not found"}

@router.get("/stats/summary")
def get_stats():
    tickets = Ticket.objects()
    stats = {"total": tickets.count(), "open": 0, "in_progress": 0, "resolved": 0, "critical": 0, "categories": {}, "priorities": {}}
    
    for t in tickets:
        if t.status == "Open": stats["open"] += 1
        elif t.status == "In Progress": stats["in_progress"] += 1
        elif t.status == "Resolved": stats["resolved"] += 1
        
        if t.priority == "Critical": stats["critical"] += 1
        
        stats["categories"][t.category] = stats["categories"].get(t.category, 0) + 1
        stats["priorities"][t.priority] = stats["priorities"].get(t.priority, 0) + 1
        
    return stats