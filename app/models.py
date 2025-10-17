from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Hijo(Base):
    __tablename__ = "hijos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    faltas = Column(Integer, default=0)
    sancion_inicio = Column(DateTime, nullable=True)

    registros = relationship("Registro", back_populates="hijo", cascade="all, delete-orphan")


class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    hijo_id = Column(Integer, ForeignKey("hijos.id"))
    tipo = Column(String)
    comentario = Column(String)
    fecha = Column(DateTime, default=datetime.now)

    hijo = relationship("Hijo", back_populates="registros")
