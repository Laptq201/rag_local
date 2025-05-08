
from test_database import connect_db



prompt = """
You are a helpful assistant. You will be provided with a query and some context. 
Your task is to generate a response based on the query and the context provided.
The context will contain relevant information that can help you answer the query.
Do not include any additional information that is not present in the context.
Your response should be concise and to the point. If the context does not provide enough information to answer the query, please state that clearly.

After you generate the response, please provide a translation to Vietnamese of your response.

"""

#I want user to input the query
query = input("Please enter your query: ")


with connect_db() as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT ai.ollama_embed('nomic-embed-text', %s, host=>'http://ollama:11434');
        """, (query,))
        query_embedding = cur.fetchone()[0]

        # Retrieve relevant documents based on cosine distance
        cur.execute("""
            SELECT title, content, 1 - (embedding <=> %s) AS similarity
            FROM documents
            ORDER BY similarity DESC
            LIMIT 2;
        """, (query_embedding,))
        rows = cur.fetchall()
                
        # Prepare the context for generating the response
        context = "\n\n".join([f"{row[0]}\nDescription: {row[1]}" for row in rows])
        print(f"Context: {context}")
        # Generate the response using the ollama_generate function
        cur.execute("""
            SELECT ai.ollama_generate('llama3.2', %s, host=>'http://ollama:11434');
        """, (f"Instructions: {prompt} Query: {query}\nContext: {context}",))
            
        model_response = cur.fetchone()[0]
        print(f"===============")
        print(model_response['response'])


