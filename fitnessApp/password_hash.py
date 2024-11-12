from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'] , deprecated=['auto']) 

def verify(plained_password , hashed_password):
    return pwd_context.verify(plained_password , hashed_password)
