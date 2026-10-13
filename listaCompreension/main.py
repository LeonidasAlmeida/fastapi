import dados
from pprint import pprint

produto = dados.produtos
# -----------------------------------------------------tecnica 1 filtro por um condição
baratos = [p for p in produto if p["preco"] < 10000]
caros = [p for p in produto if p["preco"] >= 10000]
# -----------------------------------------------------tecnica 2 procurar pelo nome
pesquisa = "rato"
resultado = [
    p for p in produto if pesquisa.lower() in p["nome"].lower()
]  # .lower() para tornar em minusculas
# -----------------------------------------------------tecnica 3 filtrar e devolver apenas determinados valores
nomes = [p["nome"] for p in produto if p["preco"] < 10000]
precos = [p["preco"] for p in produto if p["preco"] < 10000]
# -----------------------------------------------------tecnica 4 aplicar calculos aos preços
precos_com_desconto = [p["preco"] * 0.90 for p in produto]
produto_com_desconto = [
    {
        "nome": p["nome"],
        "preco_original": p["preco"],
        "preco_final": round(
            p["preco"] * 0.90, 2
        ),  # round aredonda um numero com um x, com uma precisao y
    }  #  podemos retornar lista de objectos personalizados
    for p in produto
]
# -----------------------------------------------------tecnica 5 usar if/else dentro da list comprehension
classificacao = [
    "Caro" if p["preco"] >= 10000 else "Barato" for p in produto
]  # podemos fazer operação de if else dentro dos filtros

# -----------------------------------------------------Trabalho com dicionários
# -----------------------------------------------------tecnica 6 Adicionar e atualizar propriedades
produto_item = {"id": 6, "nome": "Webcam", "preco": 15000}

# adicionar um nova propriedade
produto_item["stock"] = 12
# atualizar varios produtos
produto_item.update({"preco": 13000,"stock":20})
# -----------------------------------------------------tecnica 7 criar um dicionario apartir de uma lista
precos_por_id = {
    p["id"]:p["preco"] for p in produto
}

#pprint(precos_por_id.get(3))

# --------------------------------------------------------tecnica 8 adicionar, remover e atualizar elementos de uma lista
#Estas operações são a base de um CRUD
#Adicionar um produto
novo_produto = {
    "id":7,
    "nome":"SmartCam",
    "preco":1588,
    "stock":12
}
produto.append(novo_produto)
#Remover um produto por ID
produto_removido = [p for p in produto if p["id"] != 2] #para esse caso de remover elementos, estamos rescrevendo toda
#Atualizar por ID
for p in produto:
    if p["id"]==1:
        p["preco"]=4100
        p["stock"]=15
        break
#Encontrar por ID
produto_encontrado = next(
    (p for p in produto if p["id"] == 3), None #next retorna o primeiro resultado que encontrar, se não encontrar nada, retorna None...next(loop,None)
)
#--------------------------Estatísticas
#quantidade
quantidade = len(produto)
#maximo valor
preco_max = max(p["preco"] for p in produto)
#preço minimo
preco_min = min(p["preco"] for p in produto)
#media de valores
media = sum(p["preco"] for p in produto)/len(produto)
#valor total do stock
valor_stock = sum(p["preco"] * p["stock"] for p in produto)
pprint(round(valor_stock,2))

#lembrando que as operações feitas depois do loop são  filtro e os que vêm antes são classificação 
# Regra para memorizar:
# Objectivo	Método
#   Percorrer as chaves	data.keys()
#   Percorrer os valores	data.values()
#   Percorrer chaves e valores	data.items()
#   Obter um valor pela chave	data.get(chave)
