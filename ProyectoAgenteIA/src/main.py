from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.vectorstores import DocArrayInMemorySearch
from langchain_classic.docstore.document import Document
from langchain_classic.memory import ConversationSummaryMemory
import os


# Configuración de API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBQSf7tQJIiQOK3TWUoLcRySpUT3JkOpyk"
print("API_KEY cargada correctamente")

# Cargar modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    convert_system_message_to_human=True
)

# Información técnica y comercial puntual para evitar alucinaciones

documentos_soporte = [
    # Soluciones Técnicas
    Document(
        page_content="Problemas de Velocidad/Lentitud: Solicitar al cliente realizar un test de velocidad conectado por cable. Validar si hay equipos saturando la banda ancha (Netflix, descargas). Sugerir cambio de frecuencia a 5GHz si está en WiFi.",
        metadata={"servicio": "Internet", "tipo": "soporte"}
    ),
    Document(
        page_content="Luz Roja LOS en ONT (Módem): Explicar que es un corte de fibra. Instruir reinicio de 5 minutos. Si no levanta, informar que se requiere visita técnica para empalme de fibra.",
        metadata={"servicio": "Fibra Óptica", "tipo": "soporte"}
    ),
    Document(
        page_content="Intermitencia en horas pico: Verificar si el router está en un lugar despejado. Si el problema persiste, ofrecer actualización de firmware remota o cambio de canal WiFi.",
        metadata={"servicio": "WiFi", "tipo": "soporte"}
    ),
    Document(
        page_content="Estrategia de Retención Netlife: Si el cliente amenaza con irse a la competencia (ej. Claro o CNT), ofrecer 'Netlife Assistance' gratis por 2 meses o un descuento del 15% en la factura por el trimestre si el riesgo de deserción es ALTO.",
        metadata={"servicio": "Comercial", "tipo": "retencion"}
    ),
    Document(
        page_content="Proceso de Desconexión: No procesar la baja de inmediato. Persuadir mencionando la penalidad por retiro anticipado de equipos y la pérdida de beneficios por antigüedad antes de pasar a un supervisor.",
        metadata={"servicio": "Comercial", "tipo": "cancelacion"}
    ),

    # MATRIZ DE BENEFICIOS ECONÓMICOS Y RETENCIÓN
    Document(
        page_content="Descuento por Lealtad (Riesgo ALTO): Ofrecer 15% de descuento en la factura mensual por los próximos 4 meses.",
        metadata={"tipo": "comercial", "beneficio": "descuento"}
    ),
    Document(
        page_content="Solución Económica (Plan Flex): Si el cliente se queja del precio, ofrecer migración al 'Plan Ahorro' que reduce el costo mensual en un 20% manteniendo una velocidad estable para teletrabajo.",
        metadata={"tipo": "comercial", "beneficio": "ahorro"}
    ),
    Document(
        page_content="Bono de Velocidad Gratis: Si el cliente no quiere descuentos, ofrecer duplicar su velocidad (Speed Boost) por 3 meses sin costo adicional.",
        metadata={"tipo": "comercial", "beneficio": "regalo"}
    ),
    Document(
        page_content="Netlife Assistance Gratis: Ofrecer 3 meses de asistencia técnica especializada para computadoras sin costo (ahorro de $5.99/mes).",
        metadata={"tipo": "comercial", "beneficio": "servicio"}
    ),

    # Competencia
    Document(
        page_content="Comparativa Competencia: Si mencionan a Claro o CNT, destacar que Netlife tiene fibra óptica simétrica (misma velocidad de subida y bajada) y menor latencia para juegos y videollamadas.",
        metadata={"tipo": "comercial"}
    )
]

# Vectorización y Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
print("Embedding completado correctamente")
vectorstore = DocArrayInMemorySearch.from_documents(documentos_soporte, embeddings)
print("Documentos vectorizados correctamente")

def buscar_solucion_exacta(query: str) -> str:
    """Busca soluciones técnicas o económicas en la base de datos."""
    docs = vectorstore.similarity_search(query, k=4) # Recuperamos 4 opciones para dar variedad
    return "\n".join([d.page_content for d in docs])
    
def analizar_comportamiento_cliente(input_texto: str) -> str:
    """Herramienta de razonamiento para detectar riesgo y sentimiento."""
    prompt_analisis = f"""
    Actúa como un agente de Retención de Netlife.
    Analiza este mensaje: "{input_texto}"
    Determina: 1. Sentimiento, 2. Probabilidad de Deserción (Baja, Media, Alta), 3. ¿El cliente busca ahorro económico?
    ""
    analisis = llm.invoke(prompt_analisis)
    return analisis.content

def agendar_visita_tecnica(input_vacio: str) -> str:
    return "SISTEMA NETLIFE: Se ha generado una orden técnica prioritaria para el domicilio. Técnico asignado en 24h."

def generar_reporte_traspaso(input_vacio: str) -> str:
    # Extrae el resumen de la memoria para el supervisor humano
    resumen_actual = memoria_critica.load_memory_variables({})["chat_history"]
    return f"📋 REPORTE PARA SUPERVISOR:\n{resumen_actual}\nEstado: El cliente persiste en cancelar. Se requiere intervención humana."

# Herramientas basadas
tools = [
    Tool(name="ClasificadorDeRiesgo",
         func=analizar_comportamiento_cliente,
         description="Analiza internamente el sentimiento y riesgo de deserción."
    ),
    Tool(name="BusquedaDeSolucionesYBeneficios",
         func=buscar_solucion_exacta,
         description="Busca soluciones técnicas, descuentos y planes económicos."
    ),
    Tool(name="AgendarVisita",
         func=agendar_visita_tecnica,
         description="Genera una orden técnica si el soporte básico falla."
    ),
    Tool(name="GenerarReporteTraspaso",
         func=generar_reporte_traspaso,
         description="Genera un resumen para escalamiento si el cliente insiste en cancelar."
    )
]

# ConversationSummaryMemory para recordar acuerdos previos
memoria_critica = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    input_key="input"
)

# Instrucciones de personalidad y estrategia
prefijo_agente = """Eres el Agente Senior de Fidelización y Retención de clientes de la empresa Netlife.
Misión: Resolver problemas técnicos y ofrecer beneficios económicos para evitar la cancelación.

ESTRATEGIA:
1. Siempre usa 'ClasificadorDeRiesgo' para leer el sentimiento y para ver si el cliente está enojado o busca ahorrar.
2. Si el problema es técnico, busca en 'BusquedaDeBeneficiosYSoluciones'.
3. Si el cliente menciona que es caro o no puede pagar, ofrece el 'Plan Flex' o descuentos de lealtad o busca soluciones económicas en 'BusquedaDeSolucionesYBeneficios'.
4. Ofrece descuentos (15%) o planes de ahorro solo si detectas un riesgo de deserción ALTO o MEDIO.
5. Si el problema es técnico, primero ofrece la solución técnica y luego un pequeño bono de velocidad como cortesía.
6. Si la solución técnica falla, usa 'AgendarVisita'.
7. Si tras 3 intentos el cliente insiste en irse, usa 'GenerarReporteTraspaso'.
8. Sé muy empático. Usa frases como: 'Entiendo su situación económica' o 'Queremos que siga siendo parte de la familia Netlife"""

agente_netlife = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memoria_critica,
    verbose=True,
    agent_kwargs={'prefix': prefijo_agente},
    handle_parsing_errors=True
)

print("="*60)
print("🏢 NETLIFE CUSTOMER CARE - MODO PERSUASIVO ACTIVO")
print("="*60)

while True:
    user_input = input("\n👤 Cliente: ")
    if user_input.lower() in ["salir", "exit", "fin"]: break

    # Procesamiento con .invoke() (Basado en Practica 18)
    resultado = agente_netlife.invoke({"input": user_input})
    print(f"\n🤖 Netlife Bot: {resultado['output']}")

    # Visualización del aprendizaje del agente
    print(f"\n🧠 [Memoria de Resumen]: {memoria_critica.load_memory_variables({})['chat_history']}")
