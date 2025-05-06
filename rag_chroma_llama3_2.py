from typing import List, Dict, Any
import logging
import ollama
from ollama import chat
import chromadb
from chromadb.api.models.Collection import Collection
from rag_practice.extract_text import text_extract
from rag_practice.chunk_text import text_chunk
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("rag_system")

print("creating vector store...")
pdf_text = text_extract(pdf_path='./attention_is_all_you_need.pdf')
chunks = text_chunk(pdf_text)


documents = chunks
def setup_collection(name: str = "docs") -> Collection:
    """Set up a ChromaDB collection and populate it with document embeddings."""
    client = chromadb.Client()
    
    # Always delete collection if it exists to avoid conflicts
    try:
        client.delete_collection(name)
        logger.info(f"Deleted existing collection '{name}'")
    except Exception as e:
        logger.info(f"No existing collection to delete: {e}")
        
    # Create a new collection
    collection = client.create_collection(name=name)
    logger.info(f"Created new collection '{name}'")
    
    # Store each document in the vector embedding database
    for i, doc in enumerate(documents):
        try:
            # Get embedding from Ollama
            response = ollama.embeddings(model="nomic-embed-text", prompt=doc)
            
            # Extract embeddings from response
            if "embedding" in response:
                embeddings = response["embedding"]
            else:
                embeddings = response.get("embeddings", [])
                
            if not embeddings:
                logger.error(f"No embeddings found in response: {response}")
                raise ValueError("No embeddings found in response")
                
            # Add document to collection
            collection.add(
                ids=[str(i)],
                embeddings=[embeddings],
                documents=[doc]
            )
            logger.info(f"Added document {i} to collection")
        except Exception as e:
            logger.error(f"Error embedding document {i}: {e}")
            # Continue with next document instead of failing completely
            continue
    
    return collection

def query_and_respond(collection: Collection, query: str, model: str = "llama3.2") -> str:
    """Query the vector database and generate a response using Ollama chat API.
    
    Args:
        collection: ChromaDB collection to query
        query: The user's question
        model: The Ollama model to use for response generation
        
    Returns:
        str: The generated response
    """
    try:
        logger.info(f"Generating embedding for query: {query}")
        response = ollama.embeddings(model="nomic-embed-text", prompt=query)
        
        if "embedding" in response:
            query_embedding = response["embedding"]
        else:
            query_embedding = response.get("embeddings", [])
            
        if not query_embedding:
            logger.error(f"No embeddings found in response: {response}")
            return "Error: Could not generate embeddings for your query."
        
        logger.info("Querying vector database for relevant documents...")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2  # Get top 2 most relevant documents
        )
        
        if not results["documents"] or not results["documents"][0]:
            return "I don't have enough information to answer that question."
        
        relevant_docs = results['documents'][0]
        context = "\n".join(relevant_docs)
        logger.info(f"Found relevant documents: {context}")
        
        logger.info(f"Generating response using {model}...")
        
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful Vietnameseassistant that answers questions based on the provided context. If the context doesn't contain enough information to answer the question, say so."
            },
            {
                "role": "user",
                "content": f"Context information:\n{context}\n\nQuestion: {query}\n\nPlease answer the question based only on the context provided, and answer by VietNamese."
            }
        ]
        
        response = chat(model=model, messages=messages)
        
        # Extract the response content
        if hasattr(response, 'message') and hasattr(response.message, 'content'):
            return response.message.content
        else:
            # Fallback in case the response format changes
            return str(response)
            
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return f"Error processing query: {str(e)}"

def main():
    # Initialize the collection
    logger.info("Setting up collection...")

    collection = setup_collection()
    # Check if documents were added successfully
    try:
        count = len(collection.get()["ids"])
        logger.info(f"Collection contains {count} documents")
        if count == 0:
            logger.error("No documents were added to the collection")
            return
    except Exception as e:
        logger.error(f"Error checking collection: {e}")

    while True:
        query = input("Enter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        logger.info(f"Processing query: {query}")
        resp = query_and_respond(collection, query)
        print(f"\nQuestion: {query}\nAnswer: {resp}")


if __name__ == "__main__":
    main()