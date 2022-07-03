from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    '''This function will return the hashed password'''
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    '''This function will check wheather the passwords are same or not'''
    return pwd_context.verify(plain_password, hashed_password)





