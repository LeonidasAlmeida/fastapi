from data import produtos
from pprint import pprint


class Utill:
    lista = produtos

    def listar_por_nome_produto(self):
        return [{"cod": p["id"], "Name_product": p["nome"]} for p in self.lista]


