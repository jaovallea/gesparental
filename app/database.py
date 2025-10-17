from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ============================================================
# 📦 CONFIGURACIÓN DE BASE DE DATOS PERSISTENTE EN RENDER
# ============================================================

# Ruta persistente recomendada por Render
DB_PATH = "/opt/render/project/src/data/gesparental.db"

# Si no existe el directorio, créalo (útil en primera ejecución local)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Crear el motor de base de datos SQLite (persistente)
engine = create_engine(
    f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False}
)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base para los modelos
Base = declarative_base()
