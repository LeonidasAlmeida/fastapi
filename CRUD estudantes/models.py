from sqlalchemy import Column, Integer, String
from database import Base

class Estudante(Base):
    __tablename__ = "estudante"
    id = Column(Integer, primary_key=True,index=True)
    nome_aluno = Column(String(100),nullable=False)
    idade = Column(Integer,nullable=False)
 
class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer,primary_key=True,index=True)
    nome_curso = Column(String(200),nullable=False)
    departamento = Column(String(200),nullable=False)
    