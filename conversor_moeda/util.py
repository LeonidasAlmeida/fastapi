
from pydantic import BaseModel
from data import Data
class Utill(BaseModel):
    valor: float
    para: str
    def convertMoeda(self):
        if self.para in Data.data:
            return Data.data.get(self.para) * self.valor
        else:
            return f"não existe dados para {self.para}"




#Regra para memorizar:
#Objectivo	Método
#   Percorrer as chaves	data.keys()
#   Percorrer os valores	data.values()
#   Percorrer chaves e valores	data.items()
#   Obter um valor pela chave	data.get(chave)

