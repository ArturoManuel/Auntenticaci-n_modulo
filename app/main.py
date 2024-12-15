from fastapi import FastAPI
from app.routers import  users ,tokens
from app.models.database import engine , Base
from app.security import get_current_token

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tokens.token, prefix="/token", tags=["Token"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Slice Manager API"}
