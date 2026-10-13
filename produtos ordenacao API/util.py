from data import produtos
class Utill:
    lista = produtos
    def listar_offset(self,offset:int, limit:int):
        return sorted([p for p in self.lista[offset:limit]], key = lambda produto: produto["nome"],reverse=False)
    
test = Utill()
print(test.listar_offset(0, 3))

#sorted(
   # produtos,
   # key=lambda produto: produto["preco"]
#)