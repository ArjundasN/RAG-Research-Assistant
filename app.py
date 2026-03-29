from flask import Flask, request, jsonify
from rag import RAG
from langchain_community.document_loaders import PyPDFLoader
import os

app = Flask(__name__)

# Load documents
documents = []
data_path = "data/papers"

if not os.path.exists(data_path):
    print("❌ Folder not found:", data_path)
else:
    print("📄 Loading PDFs...")
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            documents.extend(loader.load())

print(f"✅ Loaded {len(documents)} documents")


# IMPORTANT: do NOT initialize RAG here
rag = None


@app.route("/")
def home():
    return "Flask is running"


@app.route("/query", methods=["POST"])
def query():
    global rag

    if rag is None:
        print("⚡ Initializing RAG...")
        rag = RAG(documents)

    data = request.json or {}
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    print("Query:", user_query)

    answer = rag.generate_answer(user_query)

    return jsonify({
        "query": user_query,
        "answer": answer
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,debug=True,use_reloader=False)