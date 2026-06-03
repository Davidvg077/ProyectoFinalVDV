from fastapi import APIRouter
from sqlmodel import Session, select

from database import engine
from models.categoria_model import Categoria

router = APIRouter()


@router.post("/categorias")
def crear_categoria(categoria: Categoria):
    with Session(engine) as session:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)

        return categoria


@router.get("/categorias")
def mostrar_categorias():
    with Session(engine) as session:
        categorias = session.exec(select(Categoria)).all()
        return categorias

