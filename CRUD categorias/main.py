from fastapi import FastAPI, HTTPException
import crud
from schemas import CategoriaCreate, CategoriaResponse
from database import SessionLocal,Base, engine


# Criar as tabelas que ainda não existem
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/categorias/", response_model=CategoriaResponse)
def criar_nova_categoria(categoria: CategoriaCreate):
    db = SessionLocal()
    try:
        nova_categoria = crud.criar_categoria(db, categoria)
        return nova_categoria
    finally:
        db.close()

@app.get("/categorias/", response_model=list[CategoriaResponse])
def listar_todas_categorias():
    db = SessionLocal()
    try:
        categorias = crud.listar_categoria(db)
        return categorias
    finally:
        db.close()

@app.get("/categorias/{categoria_id}", response_model=CategoriaResponse)
def obter_uma_categoria(categoria_id: int):
    db = SessionLocal()
    try:
        categoria = crud.obter_categoria(db, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        return categoria
    finally:
        db.close()

@app.put("/categorias/{categoria_id}", response_model=CategoriaResponse)
def atualizar_uma_categoria(categoria_id: int, categoria: CategoriaCreate):
    db = SessionLocal()
    try:
        categoria_existente = crud.obter_categoria(db, categoria_id)
        if not categoria_existente:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        categoria_atualizada = crud.atualizar_categoria(db, categoria_existente, categoria)
        return categoria_atualizada
    finally:
        db.close()

@app.delete("/categorias/{categoria_id}")
def deletar_uma_categoria(categoria_id: int):
    db = SessionLocal()
    try:
        categoria = crud.obter_categoria(db, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        crud.deletar_categoria(db, categoria)
        return {"message": "Categoria deletada com sucesso"}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)