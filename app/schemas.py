from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


class EmployeeCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    department: str = Field(
        min_length=1,
        max_length=100
    )

    salary: float = Field(
        ge=0
    )


class EmployeeUpdate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    department: str = Field(
        min_length=1,
        max_length=100
    )

    salary: float = Field(
        ge=0
    )


class EmployeeResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    department: str
    salary: float


class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )


class UserLogin(BaseModel):

    username: str

    password: str