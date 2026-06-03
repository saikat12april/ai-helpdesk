import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from backend.services.vector_db import process_document, get_all_files, delete_document, reload_knowledge

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    chunks = process_document(file_path, file.filename)
    return {"message": f"Successfully indexed {file.filename}", "chunks_created": chunks}

@router.get("/files")
def list_files():
    return get_all_files()

@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"uploads/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

@router.delete("/delete/{filename}")
def remove_file(filename: str):
    return {"success": delete_document(filename)}

@router.post("/reload")
def reload_files():
    return {"files_processed": reload_knowledge()}