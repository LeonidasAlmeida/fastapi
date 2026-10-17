from sqlalchemy.orm import Session
from models import Estudante,Curso
from schemas import EstudanteCreate,CursosCreate

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

#eliminar estudante
def eliminar_estudante(estudante:Estudante , db: Session ):
    db.delete(estudante)
    db.commit()
    return {"Message": "deleted with Success !"}



#--------------------------------------------------
# criar curso
def criar_curso(db: Session, dados:CursosCreate):
    curso = Curso(**dados.model_dump())
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return {"Message": "Create with Success !"}

# listar estudante
def listar_curso(db:Session):
    return db.query(Curso).all()
# pegar estudante
def obter_curso(id:int,db:Session):
    return db.get(Curso,id)
# atualizar estudante
def atualizar_curso(dados:CursosCreate,curso:Curso,db:Session):
    curso.nome_curso = dados.nome_curso
    curso.departamento = dados.departamento
    db.commit()
    db.refresh(curso)
    
#eliminar estudante
def deletar_curso(curso:Curso,db:Session):
    db.delete(curso)
    db.commit()