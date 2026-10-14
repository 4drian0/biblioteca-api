from pydantic import BaseModel, ConfigDict, Field

from app.schemas.autor import AutorResponse


class LivroCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    ano_publicacao: int = Field(ge=1000, le=2100)
    isbn: str = Field(min_length=10, max_length=17)
    autor_id: int = Field(gt=0)


class LivroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    ano_publicacao: int | None = Field(default=None, ge=1000, le=2100)
    isbn: str | None = Field(default=None, min_length=10, max_length=17)
    disponivel: bool | None = None
    autor_id: int | None = Field(default=None, gt=0)


class LivroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano_publicacao: int
    isbn: str
    disponivel: bool
    autor_id: int
    autor: AutorResponse