import os
import time

from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-2"
)

DIMENSIONS = int(
    os.getenv("EMBEDDING_DIMENSIONS", "768")
)

BATCH_SIZE = 16

MAX_RETRIES = 3


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def prepare_document_text(chunk):

    filename = chunk.get("filename", "none")

    content = chunk["content"]

    return (
        f"title: {filename} | "
        f"text: {content}"
    )


def generate_embeddings(texts):

    if not texts:
        return []

    contents = [
        types.Content(parts=[types.Part.from_text(text=text)] ) for text in texts
    ]

    for attempt in range(MAX_RETRIES):

        try:

            response = client.models.embed_content(

                model=MODEL,
                contents=contents,

                config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS)

            )

            embeddings = [
                embedding.values
                for embedding in response.embeddings
            ]

            if len(embeddings) != len(texts):
                raise ValueError(
                    "Embedding count does not match input count"
                )

            for embedding in embeddings:

                if len(embedding) != DIMENSIONS:
                    raise ValueError(
                        f"Expected {DIMENSIONS} dimensions, "
                        f"received {len(embedding)}"
                    )

            return embeddings

        except Exception:

            if attempt == MAX_RETRIES - 1:
                raise

            wait_seconds = 2 ** attempt

            print(
                f"Embedding request failed. "
                f"Retrying in {wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)


def embed_chunks(chunks):

    texts = [
        prepare_document_text(chunk)
        for chunk in chunks
    ]

    return generate_embeddings(texts)


def embed_query(query):

    query_text = (
        f"task: search result | query: {query}"
    )

    embeddings = generate_embeddings(
        [query_text]
    )

    return embeddings[0]