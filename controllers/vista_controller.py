from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from database import engine
from models.categoria_model import Categoria
from models.producto_model import Producto

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/inventario", response_class=HTMLResponse)
def pagina_inventario(request: Request):
    with Session(engine) as session:
        productos = session.exec(select(Producto)).all()
        categorias = session.exec(select(Categoria)).all()

        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "productos": productos,
                "categorias": categorias,
            },
        )

