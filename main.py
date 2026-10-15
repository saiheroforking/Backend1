from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import EmployeeCreate

app = FastAPI(title="Employee Management API")

# Allow requests from the local React development server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

employees = ["sai"]
next_id = 1


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.get("/api/employees")
def get_employees():
    return employees


@app.post("/api/employees", status_code=201)
def create_employee(employee: EmployeeCreate):
    global next_id

    if any(
        item["email"].lower() == employee.email.lower()
        for item in employees
    ):
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists",
        )

    new_employee = {
        "id": next_id,
        **employee.model_dump(),
    }

    employees.append(new_employee)
    next_id += 1

    return new_employee


@app.delete("/api/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            employees.pop(index)
            return {"message": "Employee deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Employee not found",
    )