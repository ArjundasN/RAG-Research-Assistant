import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()

#loading PDF
documents=[]
for file in os.listdir("data/papers"):
    if file.lower().endswith(".pdf"):
        file_path=os.path.join("data/papers",file)
        try:
            loader=PyPDFLoader(file_path)
            docs=loader.load()
            documents.extend(docs)
            print("Loading:", file)
        except Exception as e:
         print("Error loading", file, e)

print("Total documents loaded:", len(documents))

#text splitting
text_splitter=RecursiveCharacterTextSplitter(chunk_size=300,chunk_overlap=80)
chunks=text_splitter.split_documents(documents)
print("Chunks created:", len(chunks))
print(chunks[0].page_content[:300])

#embeddings
embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

##store in vectordb
vectorstore=PineconeVectorStore.from_documents(chunks,embeddings,index_name="rag-ai-papers")

