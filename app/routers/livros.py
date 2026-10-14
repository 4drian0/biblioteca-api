from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor, Livro
from app.schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def _validar_autor(db: Session, autor_id: int) -> None:
    """Valida a integridade: o autor referenciado precisa existir."""
    if db.get(Autor, autor_id) is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Autor com id {autor_id} não encontrado",
        )


def _validar_isbn_unico(db: Session, isbn: str, ignorar_id: int | None = None) -> None:
    existente = db.scalar(select(Livro).where(Livro.isbn == isbn))
    if existente is not None and existente.id != ignorar_id:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Já existe um livro com esse ISBN",
        )


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    _validar_autor(db, dados.autor_id)
    _validar_isbn_unico(db, dados.isbn)

    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("/", response_model=list[LivroResponse])
def listar_livros(
    autor_id: int | None = None,
    disponivel: bool | None = None,
    db: Session = Depends(get_db),
):
    consulta = select(Livro)
    if autor_id is not None:
        consulta = consulta.where(Livro.autor_id == autor_id)
    if disponivel is not None:
        consulta = consulta.where(Livro.disponivel == disponivel)
    return db.scalars(consulta).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")
    return livro


@router.patch("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")

    alteracoes = dados.model_dump(exclude_unset=True)

    if "autor_id" in alteracoes:
        _validar_autor(db, alteracoes["autor_id"])
    if "isbn" in alteracoes:
        _validar_isbn_unico(db, alteracoes["isbn"], ignorar_id=livro_id)

    for campo, valor in alteracoes.items():
        setattr(livro, campo, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")

    db.delete(livro)
    db.commit()
