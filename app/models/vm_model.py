from pydantic import BaseModel

class VM(BaseModel):
    name: str
    ip_worker: str
    status: str
