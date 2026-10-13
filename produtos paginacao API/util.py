from data import produtos
class Utill:
    lista = produtos
    def listar_offset(self,offset:int, limit:int):
        return [p for p in self.lista[offset:limit]]

