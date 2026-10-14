from app.schemas.autor import (
    AutorCreate,
    AutorDetalhe,
    AutorResponse,
    AutorUpdate,
    LivroResumo,
)
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

__all__ = [
    "AutorCreate", "AutorUpdate", "AutorResponse", "AutorDetalhe", "LivroResumo",
    "LivroCreate", "LivroUpdate", "LivroResponse",
]