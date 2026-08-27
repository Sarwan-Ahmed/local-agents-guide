"""The same 10 sentences and query as similarity_demo.py, this time through a real vector DB.

Run: python 05-vector-databases-and-embeddings/chroma_demo.py
"""

import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from similarity_demo import QUERY, SENTENCES

load_dotenv()


class OllamaEmbeddingFunction:
    """Adapts Ollama's embeddings endpoint to Chroma's embedding_function interface."""

    def __init__(self):
        self.client = OpenAI(
            base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
            api_key="not-needed",
        )
        self.model = os.environ.get("EMBED_MODEL", "nomic-embed-text")

    def __call__(self, input: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model, input=input)
        return [item.embedding for item in response.data]


def main():
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        "sentences", embedding_function=OllamaEmbeddingFunction()
    )
    collection.add(documents=SENTENCES, ids=[str(i) for i in range(len(SENTENCES))])

    results = collection.query(query_texts=[QUERY], n_results=4)

    print(f"Query: {QUERY}\n")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"{distance:.3f}  {doc}")


if __name__ == "__main__":
    main()
