from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

# Modelo para la tabla 'user'
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(45), nullable=True)
    email = Column(String(45), nullable=True)
    password = Column(String(100), nullable=True)
    rol = Column(String(45), nullable=True)
    idproject = Column(String(45), nullable=True)

    # Relación con VM
    vms = relationship("VM", back_populates="user")


# Modelo para la tabla 'worker'
class Worker(Base):
    __tablename__ = "worker"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    ip = Column(String(45), nullable=True)
    cpu_total = Column(String(45), nullable=True)
    cpu_consumer = Column(String(45), nullable=True)
    ram_total = Column(String(45), nullable=True)
    ram_consumer = Column(String(45), nullable=True)

    # Relación con VM
    vms = relationship("VM", back_populates="worker")


# Modelo para la tabla 'vm'
class VM(Base):
    __tablename__ = "vm"

    idvm = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(45), nullable=True)
    path = Column(String(45), nullable=True)
    iduser = Column(Integer, ForeignKey("user.id"), nullable=True)
    time_upload = Column(String(45), nullable=True)
    id_worker = Column(Integer, ForeignKey("worker.id"), nullable=False)

    # Relaciones con las tablas user y worker
    user = relationship("User", back_populates="vms")
    worker = relationship("Worker", back_populates="vms")
