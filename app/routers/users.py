from fastapi import APIRouter, Depends ,  HTTPException
from sqlalchemy.orm import Session
from app.services.user.user_service import get_users,create_user
from app.services.user.auth_service import authenticate_user
from app.models.database import get_db 
from app.models.models import User
from app.models.schemas import UserCreate,UserLogin
from app.security import get_current_token 
from app.tokens import TOKEN_AUTENTICACION,TOKEN_DEPLOYMENT,TOKEN_MONITOREO,TOKEN_SLICE

router = APIRouter()

# Ruta que lista todos los usuarios
@router.get("/")
def listar_usuarios(db: Session = Depends(get_db) , token: str = Depends(get_current_token) ):
    return get_users(db)



@router.post("/")
def crear_usuario(user: UserCreate, db: Session = Depends(get_db), token: str = Depends(get_current_token)):
    # Aquí podrías agregar validaciones si ya existe un usuario con el mismo nombre o correo
    return create_user(db, user)


@router.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    # Usar la función authenticate_user para autenticar al usuario
    user = authenticate_user(db, user_login)
    
    # Si la autenticación es exitosa, crear los tokens de acceso
    access_token_slice = TOKEN_SLICE
    access_token_monitoreo = TOKEN_MONITOREO
    access_token_deployment = TOKEN_DEPLOYMENT

    # Devolver la respuesta con los detalles del usuario y los tokens
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "rol": user.rol
        },
        "access_token_slice": access_token_slice,
        "access_token_monitoreo": access_token_monitoreo,
        "access_token_deployment": access_token_deployment
    }


@router.get("/validate-email/")
def validate_email(email: str, db: Session = Depends(get_db)):
    # Buscar el usuario por correo electrónico
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Devolver 'exists', 'username' y 'role' si el usuario existe
        return {"exists": True, "username": user.username, "role": user.rol}
    else:
        # Levantar excepción si el correo no está registrado
        raise HTTPException(status_code=404, detail="Correo no registrado")
