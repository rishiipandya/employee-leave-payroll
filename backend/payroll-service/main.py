from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Payroll Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

payroll = [
    {
        "id": 1,
        "employee_id": 1,
        "employee_name": "Rishi Pandya",
        "month": "October 2026",
        "basic_salary": 40000,
        "allowances": 8000,
        "deductions": 3000,
        "net_salary": 45000,
        "status": "PROCESSED"
    },
    {
        "id": 2,
        "employee_id": 2,
        "employee_name": "Rahul Manager",
        "month": "October 2026",
        "basic_salary": 60000,
        "allowances": 10000,
        "deductions": 5000,
        "net_salary": 65000,
        "status": "PROCESSED"
    }
]


@app.get("/")
def home():
    return {
        "service": "Payroll Service",
        "status": "running"
    }


@app.get("/payroll")
def get_payroll():
    return payroll


@app.get("/payroll/{employee_id}")
def get_employee_payroll(employee_id: int):
    return [
        record for record in payroll
        if record["employee_id"] == employee_id
    ]