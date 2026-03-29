from retriever import HybridRetriever
from llm import GeminiLLM
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()

os.environ["PINECONE_API_KEY"] = "pcsk_3Wx9JK_PWLMjAKjTjkhTufkn4ecmYDCXYR1X9pN6bSS92zrxgs8ksMkXUsecx6t6pDyiwe"
class RAG:
    def __init__(self,documents):
        #Load embedding model
        self.embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        #Connect to Pinecone index
        self.vector_store=PineconeVectorStore(index_name="rag-ai-papers",embedding=self.embedding_model)

        self.vector_retriever=self.vector_store.as_retriever()
        self.vector_retriever.search_kwargs = {"k": 6}

        #Hybrid retriever
        self.retriever=HybridRetriever(self.vector_retriever,documents)

        ##LLM
        self.llm=GeminiLLM()

    def generate_answer(self,query : str):    
        #retrieve docs
        docs=self.retriever.retrieve(query)
        print("Retrieved docs:", len(docs)) 
        docs = [doc for doc in docs if len(doc.page_content.strip()) > 100]
        docs = docs[:3]

        #context build
        context="\n\n".join([doc.page_content[:500] for doc in docs])

        print("---- CONTEXT ----")
        print(context[:500])
        

        #prompt
        prompt = f"""
        You are an AI assistant specialized in research papers.

        Use the provided context to answer the question accurately.

        If the answer is not found, say:
        "I don't know based on the provided research papers."

        Guidelines:
        - Explain clearly in simple terms.
        - Prefer general understanding over narrow technical wording.
        - Do not copy sentences directly; summarize in your own words.
        - Avoid overly low-level terms unless necessary (e.g., prefer "text" over "tokens" when appropriate).
        - Keep the answer concise (2-3 sentences).


        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        #response
        answer=self.llm.generate(prompt)
        return answer
    


if __name__ == "__main__":
    from langchain_community.document_loaders import PyPDFLoader
    import os

    documents = []

    for file in os.listdir("data/papers"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join("data/papers", file))
            documents.extend(loader.load())

    rag = RAG(documents)

    query = "What is semantic token clustering?"

    response = rag.generate_answer(query)

    print("\n===== FINAL ANSWER =====\n")
    print(response)