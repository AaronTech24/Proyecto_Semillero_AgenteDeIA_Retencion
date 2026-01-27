from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.memory import ConversationSummaryMemory
from langchain.agents import Tool, initialize_agent, AgentType

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    convert_system_message_to_human=True
)

documentos = [
    Document(page_content="Internet lento: revisar WiFi o usar cable"),
    Document(page_content="Luz roja LOS: posible corte de fibra"),
    Document(page_content="Descuento del 15% por fidelidad")
]

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectorstore = DocArrayInMemorySearch.from_documents(documentos, embeddings)

def buscar_solucion(query):
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])

def analizar_cliente(texto):
    return llm.invoke(f"Analiza sentimiento y riesgo: {texto}").content

tools = [
    Tool(name="ClasificadorDeRiesgo", func=analizar_cliente, description="Analiza riesgo"),
    Tool(name="BusquedaDeSoluciones", func=buscar_solucion, description="Busca soluciones")
]

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    input_key="input"
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

print("Agente IA Netlife")
while True:
    msg = input("Cliente: ")
    if msg.lower() == "salir":
        break
    response = agent.invoke({"input": msg})
    print(response["output"])
