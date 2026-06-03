from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    codigo: str = Field(primary_key=True)
    nombre: str
    stock: int
    precio: float
    categoria_id: int

