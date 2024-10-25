from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Cohere
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("La clave de API de Cohere no está configurada en las variables de entorno")

class BankingAssistant:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
        self.llm = Cohere(model="command")
        self.db = FAISS.load_local("./index", self.embeddings, allow_dangerous_deserialization=True)
        self.retriever = self.db.as_retriever()

    def get_balance(self, cedula_id):
        df = pd.read_csv("./saldos.csv")
        resultado = df[df["ID_Cedula"] == str(cedula_id)]
        if len(resultado) > 0:
            balance = resultado["Balance"].values[0]
            print(f"Pregunta: ¿Cuál es mi balance para la cédula {cedula_id}?")
            print(f"Respuesta: Su balance es {balance}")
            return balance
        else:
            return f"No se encontró balance para la cédula {cedula_id}"

    def get_banking_info(self, question):
        print(f"Pregunta: {question}")
        bank_info_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            verbose=True
        )
        respuesta = bank_info_chain.run(question)
        print(f"Respuesta: {respuesta}")
        return respuesta

    def process_query(self, query, cedula_id=None):
        print("\n--- Nueva Consulta ---")
        if "balance" in query.lower() and cedula_id:
            return self.get_balance(cedula_id)
        elif any(keyword in query.lower() for keyword in ["proceso", "cuenta", "transferencia"]):
            return self.get_banking_info(query)
        else:
            print(f"Pregunta: {query}")
            respuesta = self.llm(query)
            print(f"Respuesta: {respuesta}")
            return respuesta

asistente = BankingAssistant()
asistente.process_query("¿Cuál es mi balance?", "12345")


def main():
    asistente = BankingAssistant()
    print("¡Bienvenido al Asistente Bancario! (Escribe 'salir' para terminar)")
    
    while True:
        pregunta = input("\nHaz tu pregunta: ")
        if pregunta.lower() == 'salir':
            print("¡Gracias por usar el Asistente Bancario!")
            break
            
        if "balance" in pregunta.lower():
            cedula = input("Por favor, ingresa tu número de cédula: ")
            asistente.process_query(pregunta, cedula)
        else:
            asistente.process_query(pregunta)

if __name__ == "__main__":
    asistente = BankingAssistant()
    print("¡Bienvenido al Asistente Bancario! (Escribe 'salir' para terminar)")
    
    while True:
        pregunta = input("\nHaz tu pregunta: ")
        if pregunta.lower() == 'salir':
            print("¡Gracias por usar el Asistente Bancario!")
            break
            
        if "balance" in pregunta.lower():
            cedula = input("Por favor, ingresa tu número de cédula: ")
            asistente.process_query(pregunta, cedula)
        else:
            asistente.process_query(pregunta)