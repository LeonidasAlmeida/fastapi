from data import produtos


class Utill:
    lista = produtos

    def listar(self, categoria: str):
        return [p for p in self.lista if p["categoria"]==categoria]

