from sentence_transformers import SentenceTransformer
import chromadb
import os
from pathlib import Path


def create_collection(collection_name: str, client_path: str):
    """
    This function create chromadb collection

    :param client_path: chromadb client path (vectors folder)
    :param collection_name: Name of the collection to be created
    :return: None
    """

    try:
        collection_vectors_path = Path(client_path)
        client = chromadb.PersistentClient(path=str(collection_vectors_path))
        client.create_collection(name=collection_name)
    except Exception:
        delete_collection(collection_name, client_path)
        collection_vectors_path = Path(client_path)
        client = chromadb.PersistentClient(path=str(collection_vectors_path))
        client.create_collection(name=collection_name)
    print(f'{collection_name} collection was created. Vectors path {str(collection_vectors_path)}')


def delete_collection(collection_name: str, client_path: str):
    """
    This function delete chromadb collection

    :param client_path: chromadb client path (vectors folder)
    :param collection_name: Name of the collection to be deleted
    :return: None
    """
    client = chromadb.PersistentClient(path=str(Path(client_path)))
    client.delete_collection(name=collection_name)


def read_files_from_folder(folder_path: str):
    """
    This function getting all TXT files from folder and return TXT files name and content list

    :param folder_path: Name of the folder where the text files are located
    :return: TXT files name and content list
    """
    file_list = []

    for file_name in os.listdir(str(Path(folder_path))):
        if file_name.endswith(".txt"):
            with open(os.path.join(Path(folder_path, file_name)), 'r') as file:
                content = file.read()
                file_list.append({"file_name": file_name, "content": content})
    return file_list



def vectors_generate(collection_name, client_path, txt_documents_folder, model_name):
    """
    This function generate vectors by TXT files list

    :param collection_name: A collection where the created vectors will be added
    :param client_path: chromadb client path (vectors folder)
    :param txt_documents_folder: Name of the folder where the text files are located
    :param model_name: Model name (Default: all-mpnet-base-v2)
    :return: None
    """
    model = SentenceTransformer(model_name)
    txt_files_list = read_files_from_folder(txt_documents_folder)
    print(f'Documents list created')
    create_collection(collection_name=collection_name, client_path=client_path)

    documents = []
    embeddings = []
    metadatas = []
    ids = []
    for index, data in enumerate(txt_files_list):
        documents.append(data['content'])
        embedding = model.encode(data['content']).tolist()
        embeddings.append(embedding)
        metadatas.append({'source': data['file_name']})
        ids.append(str(index + 1)),

    client = chromadb.PersistentClient(path=str(Path(client_path)))
    collection = client.get_collection(name=collection_name)


    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

if __name__ == '__main__':
    collection_name = input("Please enter collection name: ")
    client_path = input("Please enter collection folder: ")
    txt_documents_folder = input("Please enter source TXT files folder: ")
    use_default_model_yes_no = input("Use default model ? Y/N (Default: intfloat/multilingual-e5-large: ")
    if use_default_model_yes_no.lower() == 'n':
        model_name = input("Please enter model name: ")
    else:
        model_name = "intfloat/multilingual-e5-large"
    vectors_generate(collection_name, client_path, txt_documents_folder, model_name)





