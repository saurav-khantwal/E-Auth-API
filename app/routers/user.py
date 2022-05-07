from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils
import smtplib
import random




router = APIRouter(
    prefix='/users',
    tags=['USERS']
)




# Server connection is being made to send emails

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("souravkhantwal100@gmail.com", "jsaz tvzh pwgq ekjx")





@router.post('/', status_code=status.HTTP_200_OK)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''
    
    This method will take the data from the form 
    and then Will do some validation and then
     send an OTP to the inputed email
    
    '''

    user_verify_mail = db.query(models.User).filter(
        models.User.email == user.email).first()
    user_verify_username = db.query(models.User).filter(
        models.User.username == user.username).first()

    # If email already exists in the database
    if user_verify_mail:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail='email already exists')

    # If Username already exists in the database                            
    if user_verify_username:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail='username already exists')


    # Sending OTP to the user email
    otp_number = random.randint(1000, 9999)
    server.sendmail('souravkhantwal100@gmail.com',
                    f"{user.email}", f"Your Otp for email verification is {otp_number}")

    # Payload data
    payload = {
        "user": user,
        "otp": otp_number
    }

    return payload






@router.post('/otp', status_code=status.HTTP_201_CREATED)
def verify_otp(user_data: schemas.UserOtpRegister, db: Session = Depends(get_db)):

    '''
            This method will verify the OTP provided by the user
    '''
   
    # If the OTP is verified then the User data is stored in the database
    if user_data.otp == user_data.input_otp:

        user = user_data.user
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    # Else the Exception is returned
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
