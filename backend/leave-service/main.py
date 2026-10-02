from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Leave Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeaveRequest(BaseModel):
    employee_id: int
    employee_name: str
    leave_type: str
    from_date: str
    to_date: str
    reason: str


leaves = [
    {
        "id": 1,
        "employee_id": 1,
        "employee_name": "Rishi Pandya",
        "leave_type": "Casual Leave",
        "from_date": "2026-10-05",
        "to_date": "2026-10-06",
        "reason": "Personal",
        "status": "PENDING"
    }
]


@app.get("/")
def home():
    return {
        "service": "Leave Service",
        "status": "running"
    }


@app.get("/leaves")
def get_leaves():
    return leaves


@app.get("/leaves/{employee_id}")
def get_employee_leaves(employee_id: int):
    return [
        leave for leave in leaves
        if leave["employee_id"] == employee_id
    ]


@app.post("/leaves")
def apply_leave(request: LeaveRequest):
    leave = {
        "id": len(leaves) + 1,
        **request.model_dump(),
        "status": "PENDING"
    }

    leaves.append(leave)

    return {
        "message": "Leave submitted",
        "leave": leave
    }


@app.put("/leaves/{leave_id}/approve")
def approve_leave(leave_id: int):
    for leave in leaves:
        if leave["id"] == leave_id:
            leave["status"] = "APPROVED"
            return leave

    return {
        "error": "Leave not found"
    }


@app.put("/leaves/{leave_id}/reject")
def reject_leave(leave_id: int):
    for leave in leaves:
        if leave["id"] == leave_id:
            leave["status"] = "REJECTED"
            return leave

    return {
        "error": "Leave not found"
    }