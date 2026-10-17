from sqlalchemy import Column, Integer, String
from database import Base


class Profissional(Base):
    __tablename__ = "dado_profissional"
    id = Column(Integer, primary_key=True, index=True)
    nome_funcionario = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
