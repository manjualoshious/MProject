from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
import os


# =================================
# Load Environment Variables
# =================================

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


# =================================
# MongoDB Connection
# =================================

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

print(f"{DATABASE_NAME} ✅ MongoDB Connected Successfully {MONGO_URI}")


# =================================
# Collections
# =================================

users = db["users"]
documents = db["documents"]
employees = db["employees"]


# =================================
# USER FUNCTIONS
# =================================

def add_user(username, email, password, role):

    user = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    result = users.insert_one(user)

    return {
        "message": "User registered successfully",
        "id": str(result.inserted_id)
    }


def get_user_by_email(email):

    return users.find_one({
        "email": email
    })


# =================================
# DOCUMENT FUNCTIONS
# =================================

def add_document(filename, uploaded_by, access_level,uploaded_at ):

    document = {
        "filename": filename,
        "access_level": access_level,
        "uploaded_by": uploaded_by,
        "uploaded_at": uploaded_at
    }

    result = documents.insert_one(document)

    return {
        "message": "Document uploaded successfully",
        "id": str(result.inserted_id)
    }


# =================================
# EMPLOYEE FUNCTIONS
# =================================

# -------------------------
# Add Employee
# -------------------------

def add_employee(
    username,
    email,
    password,
    role,
    department,
    designation,
    phone
):

    employee = {
        "username": username,
        "email": email,
        "password": password,
        "role": role,
        "department": department,
        "designation": designation,
        "phone": phone,
        "status": "Active",
        "created_at": datetime.now()
    }

    result = employees.insert_one(employee)

    return {
        "message": "Employee added successfully",
        "employee_id": str(result.inserted_id)
    }


# -------------------------
# Get Employee by Email
# -------------------------

def get_employee_by_email(email):

    return employees.find_one({
        "email": email
    })


def email_exists_in_users_or_employees(email):
    return (
        users.find_one({"email": email}) is not None
        or employees.find_one({"email": email}) is not None
    )


# -------------------------
# Get Employee by ID
# -------------------------

def get_employee_by_id(employee_id):

    try:
        employee = employees.find_one({
            "_id": ObjectId(employee_id)
        })

        if employee:
            employee["_id"] = str(employee["_id"])

        return employee

    except Exception:
        return None


# -------------------------
# Get All Employees
# -------------------------

def get_all_employees():

    employee_list = list(
        employees.find(
            {},
            {
                "_id": 1,
                "username": 1,
                "email": 1,
                "role": 1,
                "department": 1,
                "designation": 1,
                "phone": 1,
                "status": 1
            }
        )
    )

    for employee in employee_list:
        employee["_id"] = str(employee["_id"])

    return employee_list


# -------------------------
# Delete Employee
# -------------------------

def delete_employee(employee_id):

    try:

        result = employees.delete_one({
            "_id": ObjectId(employee_id)
        })

        if result.deleted_count == 0:
            return False

        return True

    except Exception:
        return False