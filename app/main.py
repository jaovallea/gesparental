from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .database import SessionLocal, engine
from .models import Base, Hijo, Registro

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
Base.metadata.create_all(bind=engine)


# --- Sesión DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Función para actualizar estado ---
def actualizar_estado(hijo, db: Session):
    ahora = datetime.now()

    if hijo.sancion_inicio:
        dias = (ahora - hijo.sancion_inicio).days
        if dias >= 3:
            hijo.sancion_inicio = None
            hijo.faltas = 4
            db.commit()
            return "Libre", "🔓 Salió de sanción por tiempo (faltas=4)"
        else:
            return "Sancionado", f"⏳ En sanción — faltan {3 - dias} días"
    else:
        if hijo.faltas >= 7:
            hijo.sancion_inicio = ahora
            db.commit()
            return "Sancionado", "🚫 Entró en sanción (7 faltas)"
        return "Libre", "✅ En buen estado"


# --- Calcular tablero general ---
def calcular_tablero(db: Session):
    hijos = db.query(Hijo).all()
    nombres, estado, faltas, estado_detalle, resumen, graficos, registros, totales = [], {}, {}, {}, {}, {}, {}, {}

    for hijo in hijos:
        nombres.append(hijo.nombre)
        estado[hijo.nombre], estado_detalle[hijo.nombre] = actualizar_estado(hijo, db)

        faltas[hijo.nombre] = hijo.faltas
        restantes = max(0, 7 - hijo.faltas)
        graficos[hijo.nombre] = [hijo.faltas, restantes]

        registros[hijo.nombre] = (
            db.query(Registro)
            .filter_by(hijo_id=hijo.id)
            .order_by(Registro.fecha.desc())
            .limit(10)
            .all()
        )

        hace_7_dias = datetime.now() - timedelta(days=7)
        faltas_7 = db.query(Registro).filter(
            Registro.hijo_id == hijo.id, Registro.tipo == "Falta", Registro.fecha >= hace_7_dias
        ).count()
        meritos_7 = db.query(Registro).filter(
            Registro.hijo_id == hijo.id, Registro.tipo == "Mérito", Registro.fecha >= hace_7_dias
        ).count()

        resumen[hijo.nombre] = {"faltas": faltas_7, "meritos": meritos_7}

        # ✅ Total actual (balance entre 0 y 7)
        total_actual = max(0, min(7, hijo.faltas - meritos_7))
        totales[hijo.nombre] = total_actual

    return nombres, estado, faltas, estado_detalle, resumen, graficos, registros, totales


# --- Rutas principales ---
@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    datos = calcular_tablero(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "nombres": datos[0],
        "estado": datos[1],
        "faltas": datos[2],
        "estado_detalle": datos[3],
        "resumen": datos[4],
        "graficos": datos[5],
        "registros": datos[6],
        "totales": datos[7],
    })


@app.post("/agregar")
def agregar(nombre: str = Form(...), tipo: str = Form(...), comentario: str = Form(""), db: Session = Depends(get_db)):
    comentario = comentario.strip()
    if not comentario:
        return RedirectResponse("/", status_code=303)

    hijo = db.query(Hijo).filter_by(nombre=nombre).first()
    if not hijo:
        return RedirectResponse("/", status_code=303)

    if tipo == "Falta":
        hijo.faltas = min(hijo.faltas + 1, 7)
    elif tipo == "Mérito":
        hijo.faltas = max(hijo.faltas - 1, 0)

    nuevo = Registro(hijo_id=hijo.id, tipo=tipo, comentario=comentario)
    db.add(nuevo)
    db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/borrar_registro")
def borrar_registro(id: int = Form(...), db: Session = Depends(get_db)):
    reg = db.query(Registro).filter_by(id=id).first()
    if not reg:
        return RedirectResponse("/", status_code=303)

    hijo = db.query(Hijo).filter_by(id=reg.hijo_id).first()
    if hijo:
        if reg.tipo == "Falta":
            hijo.faltas = max(hijo.faltas - 1, 0)
        elif reg.tipo == "Mérito":
            hijo.faltas = min(hijo.faltas + 1, 7)
        db.delete(reg)
        db.commit()

    return RedirectResponse("/", status_code=303)
