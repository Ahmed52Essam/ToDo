from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Input Schema (Client -> API)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


# Output Schema (API -> Client)
class UserOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"
    # Tells Pydantic to read data from ORM attributes (like user.email)
    # instead of just dictionary keys (user['email'])
    id: int
    email: EmailStr
    confirmed: bool
