from sqlalchemy.orm import Session
from models import Contacto
from schemas import ContactoCreate

#criar uma nova pessao
def criar_contacto(db: Session, dados: ContactoCreate):
    contacto = Contacto(**dados.model_dump())
    db.add(contacto)
    db.commit()
    db.refresh(contacto)
    return {"Message":"success"}

#listar contactos
def listar_contacto(db:Session):
    contacto = db.query(Contacto).all() #pesquisa todos os elemento e retorna 
    return contacto

#lista um contacto
def obter_contacto(id, db:Session):
    contacto = db.get(Contacto,id)
    return contacto

#atualizar contacto
def atualizar_contacto(contacto:Contacto, dados:ContactoCreate, db:Session):
    contacto.nome = dados.nome
    contacto.telemovel = dados.telemovel
    contacto.email = dados.email
    db.commit()
    db.refresh(contacto)
    return {"Message":"Update complete"}

#deletar contacto
def deletar_contacto(contacto: Contacto,  db:Session):
    db.delete(contacto)
    db.commit()
    return {"Message":"Delete with success !"}

 
    
    