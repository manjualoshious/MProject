from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from database.mongodb import add_user, get_user_by_email
from auth.hashing import hash_password, verify_password
from auth.jwt_handler import create_access_token
from datetime import datetime
from fastapi import UploadFile, File
from database.mongodb import (
    add_user,
    get_user_by_email,
    add_document,
    add_employee,
    get_all_employees,
    delete_employee,
    get_employee_by_email,
    email_exists_in_users_or_employees
)
import os
from services.gemini_service import ask_gemini

app = FastAPI(
    title="AI Orchestration System"
)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "AI Orchestration System API is running"
    }


# -------------------------
# User Registration Model
# -------------------------

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


# -------------------------
# Login Model
# -------------------------

class LoginUser(BaseModel):
    email: EmailStr
    password: str

# -------------------------
# Employee Model
# -------------------------

class Employee(BaseModel):

    username: str
    email: EmailStr
    password: str
    role: str
    department: str
    designation: str
    phone: str

# =================================
# Gemini Question Model
# =================================

class Question(BaseModel):

    question: str
# -------------------------
# Register
# -------------------------

@app.post("/register")
def create_user(user: User):

    # Check whether email already exists
    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password before storing
    hashed_password = hash_password(user.password)

    result = add_user(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    return result


# -------------------------
# Login
# -------------------------

@app.post("/login")
def login_user(user: LoginUser):

    # Find account in users first, then employees
    existing_user = get_user_by_email(user.email)
    account = existing_user

    if account is None:
        account = get_employee_by_email(user.email)

    if not account:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    password_correct = verify_password(
        user.password,
        account["password"]
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token({
        "email": account["email"],
        "username": account.get("username", account.get("name", "")),
        "role": account["role"]
    })

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }
# -------------------------
# Document Upload
# -------------------------

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # Create uploads folder
    upload_folder = "uploads"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    # File path
    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    # Save file
    with open(file_path, "wb") as buffer:

        buffer.write(
            await file.read()
        )

    # Save document information in MongoDB
    result = add_document(
        filename=file.filename,
        access_level="All Employees",
        uploaded_by=" unknown",
        uploaded_at=datetime.now()
        
    )

    return result
# =================================
# Ask Gemini
# =================================

@app.post("/chat")
def chat_with_gemini(data: Question):

    answer = ask_gemini(
        data.question
    )

    return {
        "question": data.question,
        "answer": answer
    }

# -------------------------
# Add Employee
# -------------------------

@app.post("/admin/employees")
def create_employee(employee: Employee):

    # Check email in both users and employees collections
    if email_exists_in_users_or_employees(employee.email):

        raise HTTPException(
            status_code=400,
            detail="Employee with this email already exists"
        )

    # Hash password
    hashed_password = hash_password(
        employee.password
    )

    result = add_employee(
        username=employee.username,
        email=employee.email,
        password=hashed_password,
        role=employee.role,
        department=employee.department,
        designation=employee.designation,
        phone=employee.phone
    )

    return result