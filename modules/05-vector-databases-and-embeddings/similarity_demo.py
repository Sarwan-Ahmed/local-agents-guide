"""Similarity search with no database -- just embeddings and cosine similarity.

Run: python 05-vector-databases-and-embeddings/similarity_demo.py
"""

import os

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SENTENCES = [
    "The chef seared the salmon in a hot cast iron pan.",
    "Astronauts on the ISS conduct experiments in microgravity.",
    "She whisked the eggs before folding them into the batter.",
    "The rover transmitted images of the Martian surface.",
    "Interest rates rose again, pushing mortgage costs higher.",
    "He grilled vegetables alongside the marinated chicken skewers.",
    "The stock market dipped after the earnings report.",
    "A new satellite was launched to study distant galaxies.",
    "The central bank signaled another rate hike next quarter.",
    "The bakery's sourdough loaf sold out within an hour.",
]

QUERY = "What's a good recipe for dinner tonight?"


def embed(client: OpenAI, model: str, texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=-1, keepdims=True)
    b_norm = b / np.linalg.norm(b)
    return a_norm @ b_norm


def main():
    client = OpenAI(
        base_url=os.environ.get("EMBED_BASE_URL", "http://localhost:11434/v1"),
        api_key="not-needed",
    )
    model = os.environ.get("EMBED_MODEL", "nomic-embed-text")

    sentence_vectors = embed(client, model, SENTENCES)
    query_vector = embed(client, model, [QUERY])[0]

    scores = cosine_similarity(sentence_vectors, query_vector)
    ranked = sorted(zip(SENTENCES, scores), key=lambda pair: pair[1], reverse=True)

    print(f"Query: {QUERY}\n")
    for sentence, score in ranked:
        print(f"{score:.3f}  {sentence}")


if __name__ == "__main__":
    main()
