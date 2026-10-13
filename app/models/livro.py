from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.autor import Autor


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    ano_publicacao: Mapped[int] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    disponivel: Mapped[bool] = mapped_column(default=True)

    # Chave estrangeira: coluna que aponta para autores.id
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"), nullable=False)

    # Um livro pertence a um autor
    autor: Mapped["Autor"] = relationship(back_populates="livros")