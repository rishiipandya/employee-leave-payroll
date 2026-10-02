from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import hashlib

app = FastAPI(title="Authentication Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "college-project-secret"

users = {
    "employee": {
        "id": 1,
        "name": "Rishi Pandya",
        "password": hashlib.sha256("1234".encode()).hexdigest(),
        "role": "EMPLOYEE"
    },
    "manager": {
        "id": 2,
        "name": "Rahul Manager",
        "password": hashlib.sha256("1234".encode()).hexdigest(),
        "role": "MANAGER"
    },
    "admin": {
        "id": 3,
        "name": "Admin",
        "password": hashlib.sha256("1234".encode()).hexdigest(),
        "role": "ADMIN"
    }
}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {
        "service": "Authentication Service",
        "status": "running"
    }


@app.post("/login")
def login(data: LoginRequest):

    user = users.get(data.username)

    password = hashlib.sha256(
        data.password.encode()
    ).hexdigest()

    if not user or user["password"] != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = jwt.encode(
        {
            "user_id": user["id"],
            "name": user["name"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "access_token": token,
        "role": user["role"],
        "user_id": user["id"],
        "name": user["name"]
    }