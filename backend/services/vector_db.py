import os
import re
from pypdf import PdfReader  # <--- FIXED: Updated from PyPDF2 to pypdf
from mongoengine import Document, StringField, ListField

class KnowledgeChunk(Document):
    filename = StringField(required=True)
    content = StringField(required=True)
    keywords = ListField(StringField())
    meta = {'collection': 'knowledge_chunks'}

def extract_keywords(text: str) -> list:
    # Extremely lightweight keyword extraction (lowercase, words > 3 chars)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return list(set(words))

def process_document(filepath: str, filename: str) -> int:
    KnowledgeChunk.objects(filename=filename).delete() # Remove old version if it exists
    text = ""
    
    if filename.endswith(".pdf"):
        reader = PdfReader(filepath)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
    # Simple chunking logic (split by paragraphs or ~500 chars)
    raw_chunks = text.split('\n\n')
    valid_chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 30]
    
    for chunk in valid_chunks:
        KnowledgeChunk(
            filename=filename,
            content=chunk,
            keywords=extract_keywords(chunk)
        ).save()
        
    return len(valid_chunks)

def search_knowledge(query: str, limit: int = 3) -> str:
    query_keywords = extract_keywords(query)
    if not query_keywords: return ""
    
    # Lightweight match scoring
    chunks = KnowledgeChunk.objects()
    scored_chunks = []
    
    for chunk in chunks:
        overlap = len(set(query_keywords).intersection(set(chunk.keywords)))
        if overlap > 0:
            scored_chunks.append((overlap, chunk.content))
            
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    top_results = [c[1] for c in scored_chunks[:limit]]
    
    return "\n---\n".join(top_results)

def get_all_files() -> dict:
    chunks = KnowledgeChunk.objects()
    filenames = list(set([c.filename for c in chunks]))
    
    files_data = []
    for fn in filenames:
        path = f"uploads/{fn}"
        size = os.path.getsize(path) if os.path.exists(path) else 0
        ext = fn.split('.')[-1].upper()
        files_data.append({"name": fn, "type": ext, "size": size})
        
    return {"total_indexed_chunks": chunks.count(), "files": files_data}

def delete_document(filename: str) -> bool:
    KnowledgeChunk.objects(filename=filename).delete()
    path = f"uploads/{filename}"
    if os.path.exists(path):
        os.remove(path)
    return True

def reload_knowledge() -> int:
    KnowledgeChunk.objects().delete()
    if not os.path.exists("uploads"):
        return 0
        
    files = os.listdir("uploads")
    for f in files:
        if not f.startswith("temp_"):
            process_document(f"uploads/{f}", f)
    return len(files)