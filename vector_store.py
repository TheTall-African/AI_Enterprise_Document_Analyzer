import chromadb

#start off with creating a persistent local Chroma database
client = chromadb.PersistentClient(path = "./chroma_db")

#create/retrieve our collection
collection = client.get_or_create_collection(name = "enterprise_documents")

def add_chunk(chunk_id, text, embedding, filename):
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadatas = [{

            "filename": filename
        }]
    )

def search_chunks(query_embedding, number_of_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],

        n_results = number_of_results
    )

    return results