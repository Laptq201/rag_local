# rag_practice

In this project, I am working on a simple RAG (Retrieval-Augmented Generation) using a PDF source. I am utilizing **Llama 3.2** as the model and the **nomic-embed-text** embedding model, along with some vector databases.

- chat_with_history.py and chat_with_history.py: Simple LLM interaction testing.
- Some utility functions for PDF processing and text embedding is in chunk_text.py, extract_text.py, and get_PDF_file.py.
- The main logic is in the rag_chroma_llama3_2.py file.

### Tasks:
- [x] Try with **ChromaDB**.
- [ ] Implement additional techniques (e.g., for table data processing).
- [ ] Other enhancements (TBD).