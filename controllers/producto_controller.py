from fastapi import APIRouter
from sqlmodel import Session, select

from database import engine
from models.producto_model import Producto

router = APIRouter()


@router.post("/productos")
def crear_producto(producto: Producto):
    with Session(engine) as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto


@router.get("/productos")
def mostrar_productos():
    with Session(engine) as session:
        productos = session.exec(select(Producto)).all()
        return productos


@router.get("/productos/{codigo}")
def buscar_producto(codigo: str):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}
        return producto


@router.put("/productos/{codigo}")
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


@router.delete("/productos/{codigo}")
def eliminar_producto(codigo: str):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}
        session.delete(producto)
        session.commit()
        return {"mensaje": "Producto eliminado correctamente"}


@router.put("/vender/{codigo}/{cantidad}")
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

        return {"mensaje": "Venta realizada", "stock_actual": producto.stock}


@router.put("/agregar-stock/{codigo}/{cantidad}")
def agregar_stock(codigo: str, cantidad: int):
    with Session(engine) as session:
        producto = session.get(Producto, codigo)
        if not producto:
            return {"mensaje": "Producto no encontrado"}

        producto.stock += cantidad

        session.add(producto)
        session.commit()
        session.refresh(producto)

        return {"mensaje": "Stock agregado", "stock_actual": producto.stock}

