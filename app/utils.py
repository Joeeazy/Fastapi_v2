from passlib.context import CryptContext

#pAssword hashing algorithmn
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return password_context.hash(password)