# app/utils.py

import jwt
import datetime
import os

# Clave secreta para firmar los tokens (debería estar en variables de entorno)
SECRET_KEY = os.getenv("SECRET_KEY", "12345")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24  # Duración del token

def create_token(user_id: int) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
