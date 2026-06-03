import os
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from mongoengine import Document, StringField, BooleanField, DateTimeField
from passlib.context import CryptContext
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_123")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE MODEL
# ══════════════════════════════════════════════════════════════════════════════
class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    department = StringField(default="General")
    role = StringField(default="employee")
    is_approved = BooleanField(default=False)  # Strict registration lock
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'users'}

# ══════════════════════════════════════════════════════════════════════════════
# REQUEST SCHEMAS
# ══════════════════════════════════════════════════════════════════════════════
class RegisterReq(BaseModel):
    name: str
    email: str
    password: str
    department: str
    role: str

class LoginReq(BaseModel):
    username: str
    password: str

class ChangePwReq(BaseModel):
    email: str
    current_password: str
    new_password: str

class ApprovalReq(BaseModel):
    approve: bool

# ══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION ROUTES
# ══════════════════════════════════════════════════════════════════════════════
@router.post("/register")
def register(req: RegisterReq):
    if User.objects(email=req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name=req.name, 
        email=req.email, 
        department=req.department,
        role=req.role, 
        is_approved=False,
        password_hash=pwd_context.hash(req.password)
    ).save()
    return {"message": "Registered successfully", "user_id": str(new_user.id)}

@router.post("/login")
def login(req: LoginReq):
    user = User.objects(email=req.username).first()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Account pending admin approval")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    expire = datetime.utcnow() + timedelta(hours=12)
    token = jwt.encode({"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token, 
        "token_type": "bearer",
        "user_name": user.name, 
        "user_role": user.role, 
        "user_email": user.email, 
        "user_id": str(user.id)
    }

@router.post("/change-password")
def change_password(req: ChangePwReq):
    user = User.objects(email=req.email).first()
    if not user or not pwd_context.verify(req.current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect current password")
    
    new_hash = pwd_context.hash(req.new_password)
    user.update(set__password_hash=new_hash)
    return {"message": "Password updated securely"}

# ══════════════════════════════════════════════════════════════════════════════
# USER MANAGEMENT ROUTES
# ══════════════════════════════════════════════════════════════════════════════
@router.get("/pending")
def get_pending():
    return [{"id": str(u.id), "name": u.name, "email": u.email, "role": u.role, "department": u.department} 
            for u in User.objects(is_approved=False)]

@router.get("/all-users")
def get_all_users():
    return [{"id": str(u.id), "name": u.name, "email": u.email, "role": u.role, "department": u.department, "is_approved": u.is_approved, "is_active": u.is_active} 
            for u in User.objects()]

@router.put("/approve/{user_id}")
def approve_user(user_id: str, req: ApprovalReq):
    user = User.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if req.approve:
        user.update(set__is_approved=True)
        return {"message": "User approved"}
    else:
        user.delete()
        return {"message": "User rejected and permanently deleted"}

@router.put("/deactivate/{user_id}")
def deactivate_user(user_id: str):
    user = User.objects(id=user_id).first()
    if user: 
        user.update(set__is_active=False)
        return {"message": "Deactivated"}
    return {"error": "User not found"}, 404

@router.delete("/delete/{user_id}")
def delete_user(user_id: str):
    user = User.objects(id=user_id).first()
    if user:
        user.delete()
        return {"message": "User permanently deleted"}
    return {"message": "User not found"}, 404