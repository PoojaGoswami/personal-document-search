
import argparse
import json

from psycopg.rows import dict_row

from database.db import get_connection
from embeddings.embedder import embed_query


def search_documents(query, top_k=5):
    # Convert the search query into an embedding
    query_embedding = embed_query(query)

    print("query_embedding-", query_embedding)

    # Convert the embedding into a format PostgreSQL understands
    query_vector = "[" + ",".join(map(str, query_embedding)) + "]"

    print("query_vector--", query_vector)

    sql = """
        SELECT
            filename,
            file_path,
            extension,
            chunk_index,
            content,
            source_locations,
            1 - (embedding <=> %s::vector) AS similarity
        FROM document_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """

    with get_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql, (query_vector, query_vector, top_k))
            results = cursor.fetchall()

    return results


def display_results(query, results):
    print(f"\nSearch query: {query}")
    print("=" * 80)

    if not results:
        print("No matching documents found.")
        return

    for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("-" * 80)

        print(f"File       : {result['filename']}")
        print(f"Type       : {result['extension']}")
        print(f"Similarity : {result['similarity']:.4f}")
        print(f"Chunk      : {result['chunk_index']}")
        print(f"Path       : {result['file_path']}")

        locations = result["source_locations"]

        if isinstance(locations, str):
            locations = json.loads(locations)

        if locations:
            print("\nSource location:")

            for location in locations:
                print(
                    f"  {location.get('location_type')}: "
                    f"{location.get('location_value')}"
                )

        content = result["content"]
        excerpt = content[:600]

        if len(content) > 600:
            excerpt += "..."

        print("\nContent:")
        print(excerpt)

    print("\n" + "=" * 80)
    print(f"Total results: {len(results)}")


def main():
    parser = argparse.ArgumentParser(
        description="Search documents using natural language"
    )

    parser.add_argument("query", help="What do you want to search for?")
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to return"
    )

    args = parser.parse_args()

    if args.top_k < 1:
        parser.error("--top-k must be greater than zero")

    try:
        results = search_documents(args.query, args.top_k)
        display_results(args.query, results)

    except Exception as e:
        print(f"\nSearch failed: {e}")
        raise


if __name__ == "__main__":
    main()
