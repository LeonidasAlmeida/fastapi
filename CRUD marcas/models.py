from sqlalchemy import Column, Integer, String
from database import Base

class Marca(Base):
    __tablename__ = "marcas"
    id = Column(Integer, primary_key = True, index = True)
    nome_marca = Column(String(100), nullable = False)
    nome_produto = Column(String(100), nullable = False)
