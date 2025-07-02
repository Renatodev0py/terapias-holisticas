from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    telefono = Column(String)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

class Servicio(Base):
    __tablename__ = "servicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    descripcion = Column(String)
    duracion_min = Column(Integer)
    precio = Column(Integer)

class Agendamiento(Base):
    __tablename__ = "agendamientos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    fecha_hora = Column(DateTime)
    estado = Column(String, default="pendiente")
