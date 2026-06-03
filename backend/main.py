import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.database import init_db

# Import all routers
from backend.routes import auth, voice, chat, tickets, assets, knowledge

load_dotenv()

app = FastAPI(title="Enterprise AI Helpdesk")

# CORS middleware for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Ensure database is initialized
    init_db()
    # Create upload directory for temporary files
    os.makedirs("uploads", exist_ok=True) 

# Register all endpoints
app.include_router(auth.router)
app.include_router(voice.router)
app.include_router(chat.router)
app.include_router(tickets.router)
app.include_router(assets.router)
app.include_router(knowledge.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Entry point for production servers
if __name__ == "__main__":
    # Render assigns a PORT dynamically
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)