from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from controllers.categoria_controller import router as categorias_router
from controllers.producto_controller import router as productos_router
from controllers.vista_controller import router as vista_router

# Import para asegurar creación de tablas al levantar la app
import database  # noqa: F401

app = FastAPI()

# Static
app.mount("/static", StaticFiles(directory="static"), name="static")


# ENDPOINT PRINCIPAL
@app.get("/")
def inicio():
    return {"mensaje": "ValeoControlX funcionando"}


# Registro de rutas (controladores)
app.include_router(vista_router)
app.include_router(categorias_router)
app.include_router(productos_router)

