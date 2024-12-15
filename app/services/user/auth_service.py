from sqlalchemy.orm import Session
from app.models.models import User
from app.models.schemas import UserLogin
from fastapi import HTTPException
from passlib.context import CryptContext

# Configuración del contexto de hash de contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear una contraseña antes de almacenarla
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar una contraseña (la recibida y la hasheada)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para autenticar al usuario
def authenticate_user(db: Session, user_login: UserLogin):
    # Buscar el usuario por username
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    # Verificar la contraseña comparando la recibida con el hash almacenado
    if not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    return user  # Devolver el objeto del usuario si la autenticación es exitosa

