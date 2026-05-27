from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlmodel import SQLModel, Field, create_engine, Session, select

from typing import Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# TABLA CATEGORIA
class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str


# TABLA PRODUCTO
class Producto(SQLModel, table=True):
    codigo: str = Field(primary_key=True)
    nombre: str
    stock: int
    precio: float
    categoria_id: int


# CONEXION POSTGRESQL
DATABASE_URL = "postgresql://postgres:Ucaodvg07480@localhost:5432/ventas"

engine = create_engine(DATABASE_URL)


# CREAR TABLAS
SQLModel.metadata.create_all(engine)


# PAGINA HTML
@app.get("/inventario", response_class=HTMLResponse)
def pagina_inventario(request: Request):
    with Session(engine) as session:
        productos = session.exec(
            select(Producto)
        ).all()
        categorias = session.exec(
            select(Categoria)
        ).all()
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "productos": productos,
                "categorias": categorias
            }
        )


# ENDPOINT PRINCIPAL
@app.get("/")
def inicio():
    return {"mensaje": "ValeoControlX funcionando"}


# CREAR CATEGORIA
@app.post("/categorias")
def crear_categoria(categoria: Categoria):
    with Session(engine) as session:
        session.add(categoria)
        session.commit()
        session.refresh(categoria)

        return categoria


# MOSTRAR CATEGORIAS
@app.get("/categorias")
def mostrar_categorias():
    with Session(engine) as session:
        categorias = session.exec(
            select(Categoria)
        ).all()

        return categorias


# CREAR PRODUCTO
@app.post("/productos")
def crear_producto(producto: Producto):
    with Session(engine) as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)

        return producto


# MOSTRAR PRODUCTOS
@app.get("/productos")
def mostrar_productos():
    with Session(engine) as session:
        productos = session.exec(
            select(Producto)
        ).all()

        return productos


# BUSCAR PRODUCTO POR CODIGO
@app.get("/productos/{codigo}")
def buscar_producto(codigo: str):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}
        return producto


# MODIFICAR PRODUCTO
@app.put("/productos/{codigo}")
def modificar_producto(codigo: str, producto_actualizado: Producto):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}

        producto.nombre = producto_actualizado.nombre
        producto.stock = producto_actualizado.stock
        producto.precio = producto_actualizado.precio
        producto.categoria_id = producto_actualizado.categoria_id

        session.add(producto)
        session.commit()
        session.refresh(producto)

        return producto


# ELIMINAR PRODUCTO
@app.delete("/productos/{codigo}")
def eliminar_producto(codigo: str):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)

        if not producto:
            return {"mensaje": "Producto no encontrado"}
        session.delete(producto)
        session.commit()
        return {"mensaje": "Producto eliminado correctamente"}


# VENDER PRODUCTO
@app.put("/vender/{codigo}/{cantidad}")
def vender_producto(codigo: str, cantidad: int):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}

        if producto.stock < cantidad:
            return {"mensaje": "Stock insuficiente"}
        producto.stock -= cantidad

        session.add(producto)
        session.commit()
        session.refresh(producto)
        return {
            "mensaje": "Venta realizada",
            "stock_actual": producto.stock
        }


# AGREGAR STOCK
@app.put("/agregar-stock/{codigo}/{cantidad}")
def agregar_stock(codigo: str, cantidad: int):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}

        producto.stock += cantidad
        session.add(producto)
        session.commit()
        session.refresh(producto)

        return {
            "mensaje": "Stock agregado",
            "stock_actual": producto.stock
        }