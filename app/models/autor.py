from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.livro import Livro


class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    nacionalidade: Mapped[str | None] = mapped_column(String(50))

    # Um autor possui vários livros
    livros: Mapped[list["Livro"]] = relationship(back_populates="autor")