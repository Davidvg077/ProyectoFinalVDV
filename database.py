from sqlmodel import SQLModel, create_engine

# CONEXIÓN PostgreSQL
DATABASE_URL = "postgresql://postgres:Ucaodvg07480@localhost:5432/ventas"

# Engine SQLModel/SQLAlchemy
engine = create_engine(DATABASE_URL)

# CREAR TABLAS
SQLModel.metadata.create_all(engine)

