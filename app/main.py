from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from .database import Base, engine, SessionLocal
from .models import Registro, Estado

# --- Configuración base ---
app = FastAPI(title="GesParental")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# --- Inicializar base de datos ---
Base.metadata.create_all(bind=engine)

# --- Parámetros generales ---
LIMITE_FALTAS = 7
DIAS_AMONESTACION = 3

# --- Funciones auxiliares ---
def iniciar_estado(db, nombre):
    estado = db.query(Estado).filter_by(nombre=nombre).first()
    if not estado:
        estado = Estado(nombre=nombre, en_amonestacion=False)
        db.add(estado)
        db.commit()
    return estado

def verificar_estado(db, nombre):
    estado = iniciar_estado(db, nombre)
    if estado.en_amonestacion and estado.fin_amonestacion:
        # si ya pasaron los 3 días y tiene 0 faltas, sale de amonestación
        faltas = db.query(Registro).filter_by(nombre=nombre, tipo="Falta").count()
        if faltas == 0 and datetime.now() >= estado.fin_amonestacion:
            estado.en_amonestacion = False
            estado.fin_amonestacion = None
            db.commit()
    return estado

def activar_amonestacion(db, nombre):
    estado = iniciar_estado(db, nombre)
    estado.en_amonestacion = True
    estado.fin_amonestacion = datetime.now() + timedelta(days=DIAS_AMONESTACION)
    db.commit()

# --- Rutas ---
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    db = SessionLocal()
    hijas = ["Johlexa", "Alejandra"]

    registros = {
        h: db.query(Registro)
        .filter(Registro.nombre == h)
        .order_by(Registro.fecha.desc())
        .all()
        for h in hijas
    }

    conteo = {
        h: db.query(Registro).filter_by(nombre=h, tipo="Falta").count() for h in hijas
    }

    estados = {h: verificar_estado(db, h) for h in hijas}

    # 🔹 Resumen de los últimos 7 días
    desde = datetime.now() - timedelta(days=7)
    resumen = {}
    for h in hijas:
        faltas = db.query(Registro).filter(
            Registro.nombre == h, Registro.tipo == "Falta", Registro.fecha >= desde
        ).count()
        meritos = db.query(Registro).filter(
            Registro.nombre == h, Registro.tipo == "Mérito", Registro.fecha >= desde
        ).count()
        resumen[h] = {"faltas": faltas, "meritos": meritos}

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "registros": registros,
            "conteo": conteo,
            "estados": estados,
            "resumen": resumen,
            "limite": LIMITE_FALTAS,
        },
    )

@app.post("/agregar")
def agregar(nombre: str = Form(...), tipo: str = Form(...), comentario: str = Form("")):
    db = SessionLocal()
    estado = verificar_estado(db, nombre)
    nuevo = Registro(nombre=nombre, tipo=tipo, comentario=comentario)
    db.add(nuevo)
    db.commit()

    if tipo == "Falta":
        faltas = db.query(Registro).filter_by(nombre=nombre, tipo="Falta").count()
        if faltas >= LIMITE_FALTAS and not estado.en_amonestacion:
            activar_amonestacion(db, nombre)

    elif tipo == "Mérito":
        # cada mérito borra una falta si hay alguna
        falta = (
            db.query(Registro)
            .filter_by(nombre=nombre, tipo="Falta")
            .order_by(Registro.fecha.asc())
            .first()
        )
        if falta:
            db.delete(falta)
            db.commit()

    verificar_estado(db, nombre)
    return RedirectResponse("/", status_code=303)

@app.post("/eliminar/{id}")
def eliminar_registro(id: int):
    db = SessionLocal()
    registro = db.query(Registro).get(id)
    if registro:
        db.delete(registro)
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/editar/{id}")
def editar_registro(id: int, tipo: str = Form(...), comentario: str = Form("")):
    db = SessionLocal()
    registro = db.query(Registro).get(id)
    if registro:
        registro.tipo = tipo
        registro.comentario = comentario
        db.commit()
    return RedirectResponse("/", status_code=303)
