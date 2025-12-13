from pydantic import BaseModel

class EmailVerificationConfirm(BaseModel):
    token: str
