from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .database import Base, engine, SessionLocal
from sqlalchemy import Column, Integer, String, DateTime
import os

# ---------------- Configuración general ----------------
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# ---------------- Modelo de datos ----------------
class Registro(Base):
    __tablename__ = "registros"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    tipo = Column(String)
    comentario = Column(String)
    fecha = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)


# ---------------- Dependencias ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Funciones auxiliares ----------------
def calcular_estado_y_resumen(registros):
    nombres = ["Johlexa", "Alejandra"]
    estado, faltas, dias_restantes, resumen, graficos, registros_dict = {}, {}, {}, {}, {}, {}

    for n in nombres:
        faltas[n] = sum(1 for r in registros if r.nombre == n and r.tipo == "Falta")
        meritos = sum(1 for r in registros if r.nombre == n and r.tipo == "Mérito")
        graficos[n] = {"faltas": faltas[n]}
        registros_dict[n] = [r for r in registros if r.nombre == n]

        # Estado sanción (7 faltas = sanción)
        if faltas[n] >= 7:
            estado[n] = "Sancionado"
            dias_restantes[n] = 3
        else:
            estado[n] = "Libre"
            dias_restantes[n] = 0

        # Resumen semanal
        hace_7_dias = datetime.now() - timedelta(days=7)
        resumen[n] = {
            "faltas": sum(1 for r in registros if r.nombre == n and r.tipo == "Falta" and r.fecha > hace_7_dias),
            "meritos": sum(1 for r in registros if r.nombre == n and r.tipo == "Mérito" and r.fecha > hace_7_dias)
        }

    return nombres, estado, faltas, dias_restantes, resumen, graficos, registros_dict


# ---------------- Rutas principales ----------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    registros = db.query(Registro).order_by(Registro.fecha.desc()).all()

    nombres, estado, faltas, dias_restantes, resumen, graficos, registros_dict = calcular_estado_y_resumen(registros)

    # Protección por defecto (si algo falla o variables están vacías)
    if not graficos:
        graficos = {n: {"faltas": 0} for n in nombres}
    if not resumen:
        resumen = {n: {"faltas": 0, "meritos": 0} for n in nombres}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "nombres": nombres,
            "estado": estado,
            "faltas": faltas,
            "dias_restantes": dias_restantes,
            "resumen": resumen,
            "graficos": graficos,
            "registros": registros_dict,
        },
    )


@app.post("/agregar")
def agregar(
    nombre: str = Form(...),
    tipo: str = Form(...),
    comentario: str = Form(""),
    db: Session = Depends(get_db)
):
    nuevo = Registro(nombre=nombre, tipo=tipo, comentario=comentario)
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/eliminar/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    reg = db.query(Registro).filter(Registro.id == id).first()
    if reg:
        db.delete(reg)
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/editar/{id}")
def editar(
    id: int,
    tipo: str = Form(...),
    comentario: str = Form(...),
    db: Session = Depends(get_db)
):
    reg = db.query(Registro).filter(Registro.id == id).first()
    if reg:
        reg.tipo = tipo
        reg.comentario = comentario
        db.commit()
    return RedirectResponse(url="/", status_code=303)
