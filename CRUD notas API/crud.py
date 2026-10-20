
from sqlalchemy.orm import Session
from models import Nota
from schemas import NotasCreate


def criar_nota(db: Session, dados: NotasCreate):
    nota = Nota(**dados.model_dump())

    db.add(nota)
    db.commit()
    db.refresh(nota)

    return nota


def listar_nota(db: Session):
    return db.query(Nota).all()


def obter_nota(db: Session, nota_id: int):
    return db.get(Nota, nota_id)


def atualizar_nota(db: Session, nota: Nota, dados: NotasCreate):
    nota.title = dados.title
    nota.comentario = dados.comentario
    db.commit()
    db.refresh(nota)

    return nota

def deletar_nota(db,nota:Nota):
    db.delete(nota)
    db.commit()
