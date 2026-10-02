from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Employee Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

employees = [
    {
        "id": 1,
        "name": "Rishi Pandya",
        "email": "rishi@example.com",
        "department": "IT",
        "designation": "Employee"
    },
    {
        "id": 2,
        "name": "Rahul Manager",
        "email": "rahul@example.com",
        "department": "IT",
        "designation": "Manager"
    }
]


@app.get("/")
def home():
    return {
        "service": "Employee Service",
        "status": "running"
    }


@app.get("/employees")
def get_employees():
    return employees


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return {
        "error": "Employee not found"
    }