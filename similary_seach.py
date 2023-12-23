from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

def similary_seach(query: str, collection_name: str, client_path, results_count: int, model_name):
    """
    This function find similary document by query

    :param query: Search query
    :param collection_name: Collection of vectors where the search will be carried out
    :param client_path: chromadb client path (vectors folder)
    :param results_count: Number of most suitable documents in descending order
    :param model_name: Model name (Default: all-mpnet-base-v2)
    :return: Sorted most suitable documents lists
    """
    model = SentenceTransformer(model_name)
    input_em = model.encode(query).tolist()
    client = chromadb.PersistentClient(path=str(Path(client_path)))
    collection = client.get_collection(name=collection_name)

    results = collection.query(
        query_embeddings=[input_em],
        n_results=results_count
    )


    # Initial data
    ids = results['ids']
    distances = results['distances']
    documents = results['documents']
    sources = results['metadatas']

    # Combining id and distance into one list
    combined = [(ids[0][i], distances[0][i], documents[0][i], sources[0][i]) for i in range(len(ids[0]))]

    # Sort the list by distance in descending order
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=False)

    return sorted_combined


if __name__ == '__main__':
    query = input("Please enter search query: ")
    results_count = input("Count of most suitable documents: ")
    collection_name = input("Please enter collection name: ")
    client_path = input("Please enter collection folder: ")
    use_default_model_yes_no = input("Use default model ? Y/N (Default: intfloat/multilingual-e5-large: ")
    if use_default_model_yes_no.lower() == 'n':
        model_name = input("Please enter model name: ")
    else:
        model_name = "intfloat/multilingual-e5-large"
    similary_seach_results = similary_seach(query, collection_name, client_path, int(results_count), model_name)
    for result in similary_seach_results:
        print(f"Vector ID: {result[0]} | Distance {result[1]} | Document name {result[3]['source']}")