# RAG Research Assistant

An AI-powered Research Assistant built using Retrieval-Augmented Generation (RAG) that allows users to query research papers and get accurate, context-aware answers.

---

##  Features

-  Ingests and processes PDF research papers
-  Semantic search using vector embeddings
-  LLM-powered answer generation
-  Fast retrieval using Pinecone vector database
-  API built with Flask
-  Interactive UI using Streamlit

---

##  Tech Stack

- Python
- LangChain
- HuggingFace Embeddings
- Pinecone (Vector DB)
- Flask (Backend API)
- Streamlit (Frontend UI)

---

##  Project Structure
RAG_capstone/
│
├── data/papers/ # Research PDFs
├── app.py # Flask API
├── ingest.py # Data ingestion & embedding
├── rag.py # RAG pipeline
├── retriever.py # Retrieval logic
├── UI.py # Streamlit UI

## Setup Instructions
- Clone the repository
- Create a .env file to store the Pinecone and Gemini API key
- download the research papers and store in data/papers using download_papers.py
- run ingest.py
- run app.py
- run UI.py

 ## Working
- PDFs are loaded and split into chunks
- Chunks are converted into embeddings
- Stored in Pinecone vector database
- User query → converted to embedding
- Relevant chunks retrieved
- LLM generates final answer


## Demonstration
<img width="1747" height="970" alt="image" src="https://github.com/user-attachments/assets/2d34bfa4-87cf-4bf5-945a-0c990f963dd9" />

