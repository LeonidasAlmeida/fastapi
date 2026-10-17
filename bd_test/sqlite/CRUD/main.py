from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from schemas import ProdutoCreate, ProdutoResponse
import crud

# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Produtos")


# Criar e fechar uma sessão por pedido
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE — criar produto
@app.post("/produtos/", response_model = ProdutoResponse, status_code=201)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db, dados)


# READ — listar produtos
@app.get("/produtos/", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return crud.listar_produtos(db)


# READ — consultar um produto
@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.obter_produto(db, produto_id)

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


# UPDATE — atualizar produto
@app.put("/produtos/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)
):
    produto = crud.obter_produto(db, produto_id)

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return crud.atualizar_produto(db, produto, dados)


# DELETE — eliminar produto
@app.delete("/produtos/{produto_id}")
def eliminar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = crud.obter_produto(db, produto_id)

    if produto is None:
        raise HTTPException(status_code = 404, detail="Produto não encontrado")

    crud.eliminar_produto(db, produto)

    return {"message": "Produto eliminado com sucesso"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
