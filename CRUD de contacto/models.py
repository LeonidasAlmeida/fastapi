from sqlalchemy import Column, String, Integer
from database import Base


class Contacto(Base):
    __tablename__ = "contactos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telemovel = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
