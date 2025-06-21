from pydantic import BaseModel

# What we want to return to the client
class Token(BaseModel): 
    access_token: str
    token_type: str ="bearer"

class TokenData(BaseModel):
    user_id: int | None = None

class LoginInput(BaseModel):
    username: str
    password: str