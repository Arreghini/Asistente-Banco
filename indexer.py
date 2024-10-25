from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# Cargar documentos individuales
docs = []
for filename in os.listdir("./knowledge_base"):
    if filename.endswith(".txt"):
        loader = TextLoader(f"./knowledge_base/{filename}")
        docs.extend(loader.load())

# Crear embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Crear y guardar la base de datos vectorial
db = FAISS.from_documents(docs, embeddings)
db.save_local("index")
