from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Crear el motor de base de datos SQLite
engine = create_engine("sqlite:///gesparental.db", connect_args={"check_same_thread": False})

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine)

# Crear la clase base para los modelos
Base = declarative_base()
