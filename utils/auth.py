import bcrypt
from email_validator import validate_email, EmailNotValidError

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def validate_email_address(email):
    try:
        valid = validate_email(email)
        return valid
    
    except EmailNotValidError:
        return None
