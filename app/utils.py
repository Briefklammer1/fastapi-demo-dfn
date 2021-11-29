from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password: str):
    return pwd_context.hash(password)

def verify_pwd(pwd_plain, pwd_hashed):
    return pwd_context.verify(pwd_plain, pwd_hashed)