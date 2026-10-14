from fastapi import FastAPI

from app.routers import autores, livros

app = FastAPI(
    title="API da Biblioteca",
    description="API para gerenciar autores e livros",
    version="1.0.0",
)

app.include_router(autores.router)
app.include_router(livros.router)


@app.get("/", tags=["Root"])
def raiz():
    return {"mensagem": "API da Biblioteca no ar! Acesse /docs"}