from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_created: datetime

    class Config:
        orm_mode = True

class UserOtp(BaseModel):
    username: str
    password: str
    user_id: str
    otp: str
    input_otp: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class OtpOut(BaseModel):
    access_token: str

class UserOtpRegister(BaseModel):
    
    user:UserCreate
    otp:str
    input_otp:str

    class Config:
        orm_mode=True