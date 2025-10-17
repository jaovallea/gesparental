from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from .database import Base


class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    comentario = Column(String)
    fecha = Column(DateTime, default=datetime.now)


class Estado(Base):
    __tablename__ = "estado_hija"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    en_amonestacion = Column(Boolean, default=False)
    fin_amonestacion = Column(DateTime, nullable=True)
