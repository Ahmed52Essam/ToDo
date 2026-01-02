from pydantic import BaseModel, ConfigDict, EmailStr


# Input Schema (Client -> API)
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Output Schema (API -> Client)
class UserOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )  # ORM mode "pydantic to be able to handle sql objects"
    # Tells Pydantic to read data from ORM attributes (like user.email)
    # instead of just dictionary keys (user['email'])
    id: int | None = None
    email: EmailStr
    confirmed: bool | None = None
