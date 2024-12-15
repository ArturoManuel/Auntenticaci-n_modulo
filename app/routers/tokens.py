from fastapi import APIRouter,  HTTPException,status 
from app.models.schemas import TokenResponse,TokenCreateRequest
from app.routers.utils import create_token
from datetime import datetime ,timedelta
from bson.objectid import ObjectId



from app.models.mondodb import db


token = APIRouter()




@token.post("/create-token", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def create_token_endpoint(request: TokenCreateRequest):
    user_id = request.user_id

    # Inactivar tokens existentes para el usuario
    await db.token.update_many(
        {"user_id": user_id, "status": True},
        {"$set": {"status": False}}
    )

    # Crear un nuevo token
    access_token = create_token(user_id)
    expire = datetime.utcnow() + timedelta(hours=24)

    token_document = {
        "user_id": user_id,
        "token": access_token,
        "created_at": datetime.utcnow(),
        "expires_at": expire,
        "status": True
    }

    result = await db.token.insert_one(token_document)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el token."
        )

    response = TokenResponse(
        user_id=user_id,
        token=access_token,
        created_at=token_document["created_at"],
        expires_at=token_document["expires_at"],
        status=token_document["status"]
    )
    return response

@token.get("/get-token/{user_id}", response_model=TokenResponse)
async def get_token_endpoint(user_id: int):
    token_doc = await db.token.find_one({"user_id": user_id, "status": True})

    if not token_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró un token activo para este usuario."
        )

    if token_doc["expires_at"] < datetime.utcnow():
        # Inactivar el token expirado
        await db.token.update_one(
            {"_id": token_doc["_id"]},
            {"$set": {"status": False}}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado."
        )

    response = TokenResponse(
        user_id=token_doc["user_id"],
        token=token_doc["token"],
        created_at=token_doc["created_at"],
        expires_at=token_doc["expires_at"],
        status=token_doc["status"]
    )
    return response