from models import Categoria
from schemas import CategoriaCreate
from sqlalchemy.orm import Session


def criar_categoria(db: Session, dados: CategoriaCreate):
    categoria = Categoria(**dados.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


def listar_categoria(db: Session):
    return db.query(Categoria).all()


def obter_categoria(db: Session, categoria_id: int):
    return db.get(Categoria, categoria_id)


def atualizar_categoria(db: Session, categoria: Categoria, dados: CategoriaCreate):
    categoria.name = dados.name
    categoria.description = dados.description
    db.commit()
    db.refresh(categoria)

    return categoria


def deletar_categoria(db: Session, categoria: Categoria):
    db.delete(categoria)
    db.commit()
    

