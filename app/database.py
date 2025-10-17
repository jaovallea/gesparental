from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Detectar si se ejecuta en Render o local
if os.getenv("RENDER") == "true":
    DB_PATH = "/opt/render/project/src/data/gesparental.db"
else:
    # Base local dentro del proyecto
    DB_PATH = os.path.join(os.path.dirname(__file__), "..", "gesparental_local.db")
    DB_PATH = os.path.abspath(DB_PATH)

# Crear el directorio si no existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Crear motor de base de datos SQLite
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base para los modelos
Base = declarative_base()
