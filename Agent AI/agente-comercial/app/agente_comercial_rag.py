import json
import unicodedata
from datetime import datetime
from pathlib import Path

import ollama
import chromadb

# ============================================================
# CONFIGURACAO
# ============================================================

MODELO_CHAT = "qwen3:4b"
MODELO_EMBEDDING = "nomic-embed-text"
FICHEIRO_VENDAS = Path("data.py")
FICHEIRO_CONHECIMENTO = Path("conhecimento.json")
PASTA_CHROMA = "./chroma_db"

# A base data.py deve conter uma lista chamada vendas:
# vendas = [
#     {"produto": "Leite Integral", "quantidade": 100,
#      "preco_unitario": 1200, "provincia": "Luanda",
#      "mes": "2026-09"}
# ]

from data import vendas


# ============================================================
# RAG: EMBEDDINGS E BASE VETORIAL
# ============================================================

cliente_chroma = chromadb.PersistentClient(path=PASTA_CHROMA)
colecao = cliente_chroma.get_or_create_collection(
    name="conhecimento_comercial"
)


def criar_embedding(texto: str) -> list[float]:
    resposta = ollama.embed(
        model=MODELO_EMBEDDING,
        input=texto
    )
    return resposta["embeddings"][0]


def carregar_conhecimento() -> list[dict]:
    if not FICHEIRO_CONHECIMENTO.exists():
        conhecimento_inicial = [
            {
                "id": "produto",
                "texto": (
                    "Produto é o artigo comercializado pela empresa. "
                    "Para encontrar o produto menos vendido, somar a "
                    "quantidade vendida por produto e ordenar de forma crescente."
                )
            },
            {
                "id": "quantidade",
                "texto": (
                    "Quantidade representa o número de unidades vendidas. "
                    "Mais vendido significa maior soma de quantidades."
                )
            },
            {
                "id": "faturacao",
                "texto": (
                    "Faturação corresponde à quantidade multiplicada pelo "
                    "preço unitário. Faturação não é lucro."
                )
            },
            {
                "id": "periodo",
                "texto": (
                    "O campo mes pode usar o formato YYYY-MM, por exemplo "
                    "2026-09. Para comparar períodos, filtrar os meses pretendidos."
                )
            }
        ]
        FICHEIRO_CONHECIMENTO.write_text(
            json.dumps(conhecimento_inicial, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    return json.loads(FICHEIRO_CONHECIMENTO.read_text(encoding="utf-8"))


def indexar_conhecimento() -> None:
    documentos = carregar_conhecimento()

    for documento in documentos:
        colecao.upsert(
            ids=[str(documento["id"])],
            documents=[str(documento["texto"])],
            embeddings=[criar_embedding(str(documento["texto"]))]
        )


def recuperar_conhecimento(pergunta: str, limite: int = 3) -> str:
    if colecao.count() == 0:
        indexar_conhecimento()

    total = colecao.count()
    limite = max(1, min(limite, total))
    embedding = criar_embedding(pergunta)

    resultado = colecao.query(
        query_embeddings=[embedding],
        n_results=limite
    )
    documentos = resultado.get("documents", [[]])[0]
    return "\n".join(documentos)


def adicionar_conhecimento(id_documento: str, texto: str) -> None:
    """Adiciona ou atualiza um documento de conhecimento empresarial."""
    colecao.upsert(
        ids=[id_documento],
        documents=[texto],
        embeddings=[criar_embedding(texto)]
    )


# ============================================================
# UTILITARIOS
# ============================================================

def normalizar(texto) -> str:
    texto = unicodedata.normalize("NFD", str(texto).lower().strip())
    return "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )


def formatar_numero(valor) -> str:
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_kz(valor) -> str:
    return f"{formatar_numero(valor)} Kz"


def e_numero(valor) -> bool:
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def obter_esquema() -> dict:
    if not vendas:
        return {}

    esquema = {}
    campos = set()
    for registo in vendas:
        campos.update(registo.keys())

    for campo in campos:
        valores = [registo.get(campo) for registo in vendas if registo.get(campo) is not None]
        esquema[campo] = {
            "tipo": type(valores[0]).__name__ if valores else "desconhecido",
            "exemplos": list(dict.fromkeys(map(str, valores)))[:8]
        }

    return esquema


def obter_campos_numericos() -> list[str]:
    esquema = obter_esquema()
    return [
        campo for campo in esquema
        if any(e_numero(registo.get(campo)) for registo in vendas)
    ]


# ============================================================
# INTERPRETACAO DA PERGUNTA COM O MODELO LOCAL
# ============================================================

def interpretar_pergunta(pergunta: str, contexto: dict) -> dict:
    esquema = obter_esquema()
    campos = list(esquema.keys())
    ano_atual = datetime.now().year
    conhecimento = recuperar_conhecimento(pergunta)

    sistema = f"""
És o planeador de consultas de um agente comercial.
Transforma a pergunta num plano de análise e devolve APENAS JSON válido.

Esquema real dos dados:
{json.dumps(esquema, ensure_ascii=False)}

Campos disponíveis:
{json.dumps(campos, ensure_ascii=False)}

Conhecimento empresarial recuperado por RAG:
{conhecimento}

Contexto da conversa:
{json.dumps(contexto, ensure_ascii=False)}

Ano atual: {ano_atual}

Estrutura obrigatória:
{{
  "tipo": "consulta | saudacao | previsao | esclarecimento",
  "metrica": "faturacao | quantidade | contar | soma | media | minimo | maximo",
  "campo_metrica": null,
  "filtros": [
    {{"campo": "campo existente", "operador": "igual | contem | prefixo | maior_que | menor_que", "valor": "valor"}}
  ],
  "agrupar_por": [],
  "ordenar_por": null,
  "ordem": "desc | asc",
  "limite": null,
  "pergunta": null
}}

REGRAS:
1. Usa apenas campos existentes no esquema real.
2. Nunca inventes registos, campos ou valores.
3. Faturação = quantidade * preco_unitario, se ambos existirem.
4. "Mais vendido" significa maior soma da quantidade.
5. "Menos vendido" significa menor soma da quantidade e ordem ascendente.
6. "Gera mais dinheiro" significa maior faturação, não lucro.
7. Para ano ou mês, filtra o campo temporal existente; mes pode usar prefixo YYYY-MM.
8. Para produtos, clientes, províncias ou vendedores, usa os campos existentes.
9. Usa agrupar_por quando a pergunta pede comparação por categoria.
10. "Top 5" implica limite 5 e ordem desc; "5 menores" implica asc.
11. Lucro exige dados de custos/margem. Se faltarem, esclarece.
12. Previsões futuras devem usar tipo previsao; não inventes previsões.
13. Se faltar informação essencial, pede esclarecimento.
14. Saudação simples usa tipo saudacao.
15. Considera o contexto anterior quando a pergunta for continuação.
16. Não devolvas SQL nem código executável.
17. O conhecimento recuperado ajuda a interpretar termos, mas não substitui os dados reais.
18. Para faturacao, campo_metrica deve ser null.
19. Para quantidade, campo_metrica deve ser "quantidade".
20. Para soma, media, minimo ou maximo, campo_metrica deve ser um campo numérico existente.
21. Para contar, conta os registos.
22. Devolve apenas JSON, sem texto adicional.
"""

    resposta = ollama.chat(
        model=MODELO_CHAT,
        messages=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": pergunta}
        ],
        format="json",
        think=False,
        options={"temperature": 0, "num_predict": 500}
    )

    plano = json.loads(resposta["message"]["content"])
    if not isinstance(plano, dict):
        raise ValueError("O modelo não devolveu um plano válido.")
    return plano


# ============================================================
# VALIDACAO E EXECUCAO DAS CONSULTAS
# ============================================================

OPERADORES_PERMITIDOS = {
    "igual", "contem", "prefixo", "maior_que", "menor_que"
}
METRICAS_PERMITIDAS = {
    "faturacao", "quantidade", "contar", "soma", "media", "minimo", "maximo"
}


def aplicar_filtros(registos: list[dict], filtros: list[dict]) -> list[dict]:
    if not isinstance(filtros, list):
        raise ValueError("Os filtros têm de ser uma lista.")

    campos = set().union(*(r.keys() for r in registos)) if registos else set()
    resultado = list(registos)

    for filtro in filtros:
        if not isinstance(filtro, dict):
            raise ValueError("Cada filtro deve ser um objeto.")
        campo = filtro.get("campo")
        operador = filtro.get("operador")
        valor = filtro.get("valor")

        if campo not in campos:
            raise ValueError(f"Campo inexistente: {campo}")
        if operador not in OPERADORES_PERMITIDOS:
            raise ValueError(f"Operador não permitido: {operador}")
        if valor is None:
            raise ValueError("O filtro não contém valor.")

        novos = []
        for registo in resultado:
            atual = registo.get(campo)
            corresponde = False

            if atual is None:
                corresponde = False
            elif operador == "igual":
                if e_numero(atual):
                    try:
                        corresponde = float(atual) == float(valor)
                    except (ValueError, TypeError):
                        corresponde = False
                else:
                    corresponde = normalizar(atual) == normalizar(valor)
            elif operador == "contem":
                corresponde = normalizar(valor) in normalizar(atual)
            elif operador == "prefixo":
                corresponde = normalizar(atual).startswith(normalizar(valor))
            else:
                try:
                    a, b = float(atual), float(valor)
                    corresponde = a > b if operador == "maior_que" else a < b
                except (ValueError, TypeError):
                    corresponde = False

            if corresponde:
                novos.append(registo)
        resultado = novos

    return resultado


def valor_metrica(registo: dict, metrica: str, campo_metrica: str | None):
    if metrica == "faturacao":
        if not {"quantidade", "preco_unitario"}.issubset(registo):
            raise ValueError("Faltam quantidade ou preco_unitario para calcular faturação.")
        return float(registo["quantidade"]) * float(registo["preco_unitario"])

    if metrica == "quantidade":
        campo_metrica = "quantidade"

    if metrica in {"soma", "media", "minimo", "maximo", "quantidade"}:
        if not campo_metrica or campo_metrica not in registo:
            raise ValueError(f"Campo numérico inexistente: {campo_metrica}")
        valor = registo[campo_metrica]
        if not e_numero(valor):
            raise ValueError(f"O campo {campo_metrica} não é numérico.")
        return float(valor)

    raise ValueError(f"Métrica não suportada: {metrica}")


def calcular_resultado(registos: list[dict], metrica: str, campo_metrica: str | None):
    if metrica == "contar":
        return len(registos)

    valores = [
        valor_metrica(registo, metrica, campo_metrica)
        for registo in registos
    ]
    if not valores:
        return 0

    if metrica in {"faturacao", "quantidade", "soma"}:
        return sum(valores)
    if metrica == "media":
        return sum(valores) / len(valores)
    if metrica == "minimo":
        return min(valores)
    if metrica == "maximo":
        return max(valores)
    raise ValueError(f"Métrica não suportada: {metrica}")


def executar_consulta(plano: dict) -> str:
    if not vendas:
        return "A base de dados não contém registos de vendas."

    tipo = plano.get("tipo")
    if tipo == "saudacao":
        return "Olá! Posso analisar os dados comerciais. O que gostarias de descobrir?"
    if tipo == "previsao":
        return (
            "Ainda não existe um modelo de previsão implementado. "
            "Posso analisar os dados históricos, mas não vou inventar vendas futuras."
        )
    if tipo == "esclarecimento":
        return plano.get("pergunta") or "Preciso de mais informações para responder com segurança."
    if tipo != "consulta":
        return "Não consegui criar uma consulta válida para esta pergunta."

    metrica = plano.get("metrica", "faturacao")
    if metrica not in METRICAS_PERMITIDAS:
        raise ValueError("Métrica não permitida.")

    filtros = plano.get("filtros", [])
    registos = aplicar_filtros(vendas, filtros)
    campo_metrica = plano.get("campo_metrica")
    agrupamentos = plano.get("agrupar_por") or []

    if not isinstance(agrupamentos, list):
        raise ValueError("Os agrupamentos têm de ser uma lista.")

    campos = set().union(*(r.keys() for r in vendas)) if vendas else set()
    for campo in agrupamentos:
        if campo not in campos:
            raise ValueError(f"Campo de agrupamento inexistente: {campo}")

    if not registos:
        return "Não encontrei registos que correspondam aos filtros pedidos."

    if not agrupamentos:
        total = calcular_resultado(registos, metrica, campo_metrica)
        if metrica == "faturacao":
            valor = formatar_kz(total)
        elif metrica == "contar":
            valor = str(total)
        else:
            valor = formatar_numero(total)
        return f"Resultado: {valor} ({len(registos)} registos analisados)."

    grupos = {}
    for registo in registos:
        chave = tuple(registo.get(campo) for campo in agrupamentos)
        grupos.setdefault(chave, []).append(registo)

    resultados = []
    for chave, itens in grupos.items():
        valor = calcular_resultado(itens, metrica, campo_metrica)
        resultados.append((chave, valor))

    ordem = plano.get("ordem", "desc")
    if ordem not in {"asc", "desc"}:
        ordem = "desc"

    resultados.sort(key=lambda item: item[1], reverse=(ordem == "desc"))

    limite = plano.get("limite")
    if isinstance(limite, int) and not isinstance(limite, bool) and 1 <= limite <= 100:
        resultados = resultados[:limite]

    linhas = []
    for chave, valor in resultados:
        nome = " | ".join(
            f"{campo}: {valor_campo}"
            for campo, valor_campo in zip(agrupamentos, chave)
        )
        valor_formatado = formatar_kz(valor) if metrica == "faturacao" else formatar_numero(valor)
        linhas.append(f"- {nome}: {valor_formatado}")

    return "Resultados da análise:\n" + "\n".join(linhas)


# ============================================================
# INTERFACE DE CONVERSA
# ============================================================

def perguntar_agente(pergunta: str, contexto: dict):
    try:
        plano = interpretar_pergunta(pergunta, contexto)
        resposta = executar_consulta(plano)
        novo_contexto = {
            "ultima_pergunta": pergunta,
            "ultimo_plano": plano
        }
        return resposta, novo_contexto
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as erro:
        return f"Não consegui executar a análise com segurança: {erro}", contexto
    except Exception as erro:
        return f"Ocorreu um erro ao consultar o agente: {erro}", contexto


def main():
    # Indexa o conhecimento ao iniciar. Para atualizar o conhecimento,
    # edita conhecimento.json e volta a executar o programa.
    indexar_conhecimento()
    print("Agente comercial com RAG iniciado.")
    print("Escreve 'sair' para terminar.\n")

    contexto = {}
    while True:
        try:
            pergunta = input("Pergunta comercial: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if normalizar(pergunta) == "sair":
            print("Até logo!")
            break
        if not pergunta:
            continue

        resposta, contexto = perguntar_agente(pergunta, contexto)
        print(f"\nAgente:\n{resposta}\n")


if __name__ == "__main__":
    main()
