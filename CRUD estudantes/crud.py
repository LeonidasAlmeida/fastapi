from sqlalchemy.orm import Session
from models import Estudante
from schemas import EstudanteCreate, EstudanteResponse


# criar estudante
def criar_estudante(db: Session, dados: EstudanteCreate):
    estudante = Estudante(**dados.model_dump())
    db.add(estudante)
    db.commit()
    db.refresh(estudante)

    return {"Message": "Create with Success !"}


# listar estudante
def listar_estudante(db: Session):
    estudante = db.query(Estudante).all()
    return estudante


# pegar estudante
def obter_estudante(id: int, db: Session):
    return db.get(Estudante, id)


# atualizar estudante
def atualizar_estudante(dados: EstudanteCreate, estudante:Estudante, db: Session):
    estudante.nome_aluno = dados.nome_aluno
    estudante.idade = dados.idade
    db.commit()
    db.refresh(estudante)
    return {"Message": "Update with Success !"}


