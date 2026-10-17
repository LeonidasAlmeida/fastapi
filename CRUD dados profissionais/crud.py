from sqlalchemy.orm import Session
from models import Profissional
from schemas import ProfissionalCreate

#criar profissional
def criar_prof(db: Session, dados : ProfissionalCreate):
    prof  = Profissional(**dados.model_dump())
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return {"Message":"Create With Success !"}

#listar prfissional
def listar_prof(db: Session):
    return db.query(Profissional).all()

            
#obter profissional
def obter_prof(id:int, db: Session):
    return db.get(Profissional,id)

#atualizar profissional
def atualizar_prof(dados:ProfissionalCreate,prof:Profissional,db:Session):
    prof.nome_funcionario = dados.nome_funcionario
    prof.cargo = dados.cargo
    
    db.commit()
    db.refresh(prof)
    return {"Message":"Update With Success !"}
#eliminar profissional
def deletar_prof(prof:Profissional,db:Session):
    db.delete(prof)
    db.commit()
    
