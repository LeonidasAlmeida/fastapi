from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from schemas import CategoriaCreate, CategoriaResponse
import crud
from typing import Generator

# criar tabelas
Base.metadata.create_all(bind=engine)
# criar o servidor
app = FastAPI(title="API de Marcas")


# Criar e fechar uma sessão por pedido
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rotas
# Rota para criar marcas
@app.post("/marcas/")
def criar_marca(dados: CategoriaCreate, db: Session = Depends(get_db)):
    return crud.criar_marca(dados, db)


# Rota para listar marcas
@app.get("/marcas/", response_model=list[CategoriaResponse])
def listar_marcas(db: Session = Depends(get_db)):
    return crud.listar_marcas(db)


# Rota para obter marca
@app.get("/marcas/pegar/", response_model=CategoriaResponse)
def obter_marcas(id: int, db: Session = Depends(get_db)):
    marca = crud.obter_marca(id, db)
    if marca is None:
        raise HTTPException(status_code = 404, detail = "Marca não encontrada")
    return marca
# Rota para atualizar marca
@app.put("/marcas/")
def atualizar_marcas(dados: CategoriaCreate, id:int , db: Session = Depends(get_db)):
    marca = crud.obter_marca(id, db)
    if marca is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    return crud.atualizar_marca(dados, marca, db    )
# Rota para deletar marca
@app.delete("/marcas/")
def deletar_marcas(id:int, db: Session = Depends(get_db)):
    marca = crud.obter_marca(id, db)
    if marca is None:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    return crud.deletar_marca(marca, db)

# verificar variavel de inicialização do servidor
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
