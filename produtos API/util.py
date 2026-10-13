from data import produtos
class Utill:
    lista = produtos
    def listar(self):
        return [p for p in self.lista]

