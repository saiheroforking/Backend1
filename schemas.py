from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    department: str = Field(min_length=2, max_length=100)