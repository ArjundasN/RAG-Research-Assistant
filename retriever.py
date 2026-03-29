from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document

class HybridRetriever:
    def __init__(self,vector_retriever,documents):
        self.vector_retriever=vector_retriever
        clean_docs = []

        for i, doc in enumerate(documents):
         clean_docs.append(
         Document(
            page_content=doc.page_content,
            metadata=doc.metadata,
            id=str(i) 
        )
    )
        self.bm25=BM25Retriever.from_documents(clean_docs)
        self.bm25.k=4

    def retrieve(self,query):
        bm25_docs=self.bm25.invoke(query)
        vector_docs=self.vector_retriever.invoke(query)

        print("BM25 docs:", len(bm25_docs))
        print("Vector docs:", len(vector_docs))

        combined = vector_docs + bm25_docs

        unique_docs={}
        for doc in combined:    
            key = doc.metadata.get("source", "") + str(doc.metadata.get("page", ""))
            unique_docs[key] = doc

        return list(unique_docs.values())[:5]