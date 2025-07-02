from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from pydantic import BaseModel
import os, requests
from dotenv import load_dotenv

load_dotenv()
WEBSERVICE_URL = os.getenv("WEBSERVICE_URL")

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ClienteIn(BaseModel):
    nombre: str
    correo: str
    telefono: str

@app.post("/registro")
def registrar(c: ClienteIn, db: Session = Depends(get_db)):
    cliente = models.Cliente(**c.dict())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return {"cliente_id": cliente.id}

class AgendarIn(BaseModel):
    cliente_id: int
    servicio_id: int
    fecha_hora: str

@app.post("/agendar")
def agendar(a: AgendarIn, db: Session = Depends(get_db)):
    agenda = models.Agendamiento(**a.dict())
    db.add(agenda)
    db.commit()
    db.refresh(agenda)
    return {"agenda_id": agenda.id, "estado": agenda.estado}

@app.get("/servicios")
def listar_servicios(db: Session = Depends(get_db)):
    return db.query(models.Servicio).all()

@app.post("/pagar/{agenda_id}")
def pagar(agenda_id: int, db: Session = Depends(get_db)):
    agenda = db.query(models.Agendamiento).filter_by(id=agenda_id).first()
    if not agenda:
        raise HTTPException(404, "No existe agendamiento")
    servicio = db.query(models.Servicio).get(agenda.servicio_id)
    payload = {
        "amount": servicio.precio,
        "buy_order": str(agenda.id),
        "session_id": str(agenda.cliente_id),
        "return_url": os.getenv("RETURN_URL")
    }
    r = requests.post(f"{WEBSERVICE_URL}/transactions", json=payload)
    return r.json()
