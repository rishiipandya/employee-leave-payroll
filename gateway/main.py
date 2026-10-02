import os
import jwt
import httpx

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="Employee Management API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "college-project-secret"

SERVICES = {
    "auth": os.getenv("AUTH_URL", "http://localhost:8001"),
    "employee": os.getenv("EMPLOYEE_URL", "http://localhost:8002"),
    "leave": os.getenv("LEAVE_URL", "http://localhost:8003"),
    "payroll": os.getenv("PAYROLL_URL", "http://localhost:8004"),
}


@app.get("/")
def home():
    return {
        "service": "API Gateway",
        "status": "running",
        "services": list(SERVICES.keys())
    }


def get_token(request: Request):
    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    token = authorization.split(" ", 1)[1]

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def require_role(request: Request, roles):
    user = get_token(request)

    if user.get("role") not in roles:
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions"
        )

    return user


async def forward(request: Request, service: str, path: str):
    url = SERVICES[service] + path

    body = await request.body()

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ["host", "content-length"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            url,
            content=body,
            headers=headers
        )

    try:
        content = response.json()
    except Exception:
        content = {
            "message": response.text
        }

    return JSONResponse(
        content=content,
        status_code=response.status_code
    )


# ---------------- AUTH ----------------

@app.api_route(
    "/auth/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE"]
)
async def auth(request: Request, path: str):
    return await forward(
        request,
        "auth",
        "/" + path
    )


# ---------------- EMPLOYEE ----------------

@app.get("/employees")
async def employees_root(request: Request):
    get_token(request)

    return await forward(
        request,
        "employee",
        "/employees"
    )


@app.get("/employees/{path:path}")
async def employees(request: Request, path: str):
    get_token(request)

    return await forward(
        request,
        "employee",
        "/employees/" + path
    )


# ---------------- LEAVE ----------------

@app.get("/leaves")
async def leaves_root(request: Request):
    get_token(request)

    return await forward(
        request,
        "leave",
        "/leaves"
    )


@app.post("/leaves")
async def apply_leave(request: Request):
    get_token(request)

    return await forward(
        request,
        "leave",
        "/leaves"
    )


@app.get("/leaves/{employee_id}")
async def employee_leaves(
    request: Request,
    employee_id: int
):
    get_token(request)

    return await forward(
        request,
        "leave",
        f"/leaves/{employee_id}"
    )


@app.put("/leaves/{leave_id}/approve")
async def approve_leave(
    request: Request,
    leave_id: int
):
    require_role(request, ["MANAGER", "ADMIN"])

    return await forward(
        request,
        "leave",
        f"/leaves/{leave_id}/approve"
    )


@app.put("/leaves/{leave_id}/reject")
async def reject_leave(
    request: Request,
    leave_id: int
):
    require_role(request, ["MANAGER", "ADMIN"])

    return await forward(
        request,
        "leave",
        f"/leaves/{leave_id}/reject"
    )


# ---------------- PAYROLL ----------------

@app.get("/payroll")
async def payroll_root(request: Request):
    require_role(request, ["MANAGER", "ADMIN"])

    return await forward(
        request,
        "payroll",
        "/payroll"
    )


@app.get("/payroll/{employee_id}")
async def employee_payroll(
    request: Request,
    employee_id: int
):
    get_token(request)

    return await forward(
        request,
        "payroll",
        f"/payroll/{employee_id}"
    )