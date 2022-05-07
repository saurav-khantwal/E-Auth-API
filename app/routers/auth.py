from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import smtplib
import random




router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)




# Here the SMTP sever connection is made to send emails

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("souravkhantwal100@gmail.com", "jsaz tvzh pwgq ekjx")





@router.post('/', status_code=status.HTTP_200_OK)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    '''

        This function will take the input credentials and verify them
        after that it will send an otp to the users email for further verification

    '''

    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid username')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')

    
    # Here OTP is being sent to the user email
    otp_number = random.randint(1000, 9999)
    server.sendmail('souravkhantwal100@gmail.com',
                    f"{user.email}", f"Your OTP for secure login is {otp_number}")

    # Payload is being returned as a response
    return_payload = {"username":user.username, "password":user.password, "otp":otp_number}
    return return_payload






@router.post('/otp', status_code=status.HTTP_202_ACCEPTED)
def verify_otp(user: schemas.UserOtp, db: Session = Depends(database.get_db)):

    '''
    
        This function will verify the otp provided by the user and then it will 
        return a JWT token for the user as a response

    '''
   
    if user.otp == user.input_otp:
        return {"access_token": "your token"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid otp')
