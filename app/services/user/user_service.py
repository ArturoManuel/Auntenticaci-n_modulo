from sqlalchemy.orm import Session
from app.models.models import User
from app.models.schemas import UserCreate
from app.services.user.auth_service import hash_password

# Asegúrate de que la función reciba la sesión de la base de datos (db)
def get_users(db: Session):
    # Realizar la consulta a la tabla User
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)  # Hashear la contraseña
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,  # Almacenar la contraseña hasheada
        rol=user.rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




