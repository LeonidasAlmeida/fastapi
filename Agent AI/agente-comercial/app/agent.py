
import json
import ollama
import chromadb

MODELO_EMBEDDING = "nomic-embed-text"

cliente = chromadb.PersistentClient(
    path="./chroma_db"
)

colecao = cliente.get_or_create_collection(
    name="conhecimento_comercial"
)


def criar_embedding(texto: str):
    resposta = ollama.embed(
        model=MODELO_EMBEDDING,
        input=texto
    )
    return resposta["embeddings"][0]


def indexar_conhecimento():
    with open(
        "conhecimento.json",
        "r",
        encoding="utf-8"
    ) as ficheiro:
        documentos = json.load(ficheiro)

    for documento in documentos:
        colecao.upsert(
            ids=[documento["id"]],
            documents=[documento["texto"]],
            embeddings=[
                criar_embedding(documento["texto"])
            ]
        )


def recuperar_conhecimento(pergunta: str, limite: int = 3):
    embedding = criar_embedding(pergunta)

    resultado = colecao.query(
        query_embeddings=[embedding],
        n_results=limite
    )

    documentos = resultado["documents"][0]

    return "\n".join(documentos)


if __name__ == "__main__":
    indexar_conhecimento()
    print("Conhecimento indexado com sucesso.")

    pergunta = "Como descobrir o produto menos vendido?"
    print(recuperar_conhecimento(pergunta))
