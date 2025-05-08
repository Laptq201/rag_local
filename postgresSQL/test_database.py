import psycopg2
import re



def connect_db():
    return psycopg2.connect( 
        host = 'localhost',
        database = 'postgres',
        user = 'postgres',
        password = 'password',
        port = '5433' 
    )


def create_table():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    content TEXT,
                    embedding VECTOR(768)
                );
            """)  


def sanitize_text(text):
    """Remove invalid characters (NUL, control characters)."""
    if not isinstance(text, str):
        text = str(text)
    # Remove non-printable characters except newlines and tabs
    return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', text).strip()

def preprocess_dummy_data(dummy_data):
    """Sanitize titles and content fields."""
    return [
        {
            "title": sanitize_text(doc["title"]),
            "content": sanitize_text(doc["content"])
        }
        for doc in dummy_data
    ]

 
def add_dummy_data(dummy_data):
    create_table()  # Ensure the table exists
    sanitized_data = preprocess_dummy_data(dummy_data)  # Preprocess
    print(sanitized_data[0])
    with connect_db() as conn:
        with conn.cursor() as cur:
            for doc in sanitized_data:
                try:
                    # Check for empty content/title
                    if not doc["content"] or not doc["title"]:
                        print(f"Skipping invalid document: {doc}")
                        continue
                    
                    # Insert with sanitized data
                    cur.execute("""
                        INSERT INTO documents (title, content, embedding)
                        VALUES (
                            %(title)s,
                            %(content)s,
                            ai.ollama_embed(
                                'nomic-embed-text', 
                                concat(%(title)s, ' - ', %(content)s), 
                                host=>'http://ollama:11434'
                            )
                        );
                    """, doc)
                except Exception as e:
                    print(f"Failed to insert document: {doc}")
                    print(f"Error: {e}")
                    conn.rollback()  # Rollback on failure
                    raise
            conn.commit()  # Commit only if all inserts succeed
                        


def delete_data_in_postgres():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM documents;")
            conn.commit()
            print("Data deleted successfully.")
     
