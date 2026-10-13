from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# O SQLite exige esse argumento para funcionar com várias threads (FastAPI)
connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe base da qual todos os modelos herdam."""


def get_db():
    """Dependência: abre uma sessão por requisição e garante que feche."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()