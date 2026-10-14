from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor
from app.schemas import AutorCreate, AutorDetalhe, AutorResponse, AutorUpdate

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.post("/", response_model=AutorResponse, status_code=status.HTTP_201_CREATED)
def criar_autor(dados: AutorCreate, db: Session = Depends(get_db)):
    autor = Autor(**dados.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


@router.get("/", response_model=list[AutorResponse])
def listar_autores(db: Session = Depends(get_db)):
    return db.scalars(select(Autor)).all()


@router.get("/{autor_id}", response_model=AutorDetalhe)
def buscar_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor não encontrado")
    return autor


@router.patch("/{autor_id}", response_model=AutorResponse)
def atualizar_autor(autor_id: int, dados: AutorUpdate, db: Session = Depends(get_db)):
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor não encontrado")

    # exclude_unset: só altera o que o cliente realmente enviou
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)

    db.commit()
    db.refresh(autor)
    return autor


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Autor não encontrado")

    if autor.livros:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Não é possível excluir um autor que possui livros cadastrados",
        )

    db.delete(autor)
    db.commit()