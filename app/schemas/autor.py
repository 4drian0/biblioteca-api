from pydantic import BaseModel, ConfigDict, Field


class AutorCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    nacionalidade: str | None = Field(default=None, max_length=50)


class AutorUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    nacionalidade: str | None = Field(default=None, max_length=50)


class AutorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    nacionalidade: str | None


class LivroResumo(BaseModel):
    """Versão enxuta do livro, usada dentro da resposta do autor."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publicacao: int


class AutorDetalhe(AutorResponse):
    """Autor + lista de seus livros (usa o relationship)."""
    livros: list[LivroResumo] = []