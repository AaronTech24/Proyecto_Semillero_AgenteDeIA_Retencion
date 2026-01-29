# Grupo: Los Hackers de IA

## Agente IA [Agente Clasificador de Riesgo de Deserción]
### Descripción breve del proyecto: 
Se deberá crear un agente LLM para poder gestionar una conversación sobre problemas de servicio de internet, este debe gestionar la mala actitud del cliente, persuadir y analizar el léxico y sentimiento de la conversación y poder indicar el probabilidad de deserción / cancelación del servicio.

## Integrantes
- Tirado Mendoza Kelvin Aarón @AaronTech24
- Delgado Quiñonez Elian Adonis @Delgado-Elian
- Zambrano Mendoza Jeremy Dario @Jerzom
- Vasquez Gorozabel Ryan Manuel @Ryan401-byte
- Palma Piguave Daniel Vicente @danielpalma54
- Anzules Rivera Paulina Michelle @Paulinaanz22
- Montesinos Villavicencio Saúl Efraín @deathsoul-04


## Descripción
### [Qué hace el agente]
- Link del video: youtube, Google Drive.


# 🚀 Agente IA: Clasificador de Riesgo de Deserción (Netlife)

Este proyecto implementa un agente inteligente basado en **LangChain** y **Google Gemini** diseñado para la retención de clientes de servicios de internet. El agente no solo resuelve problemas técnicos, sino que analiza el sentimiento del usuario, evalúa el riesgo de cancelación y aplica estrategias comerciales persuasivas.

## 🛠️ Arquitectura del Sistema

El agente utiliza una arquitectura híbrida que combina:

* **RAG (Retrieval-Augmented Generation):** Para consultas técnicas y comerciales exactas.
* **Agentic Reasoning (ReAct):** Para decidir qué herramientas usar según la situación.
* **Conversational Summary Memory:** Para aprender del historial y resumir casos críticos.

## 📝 Documentación de Módulos (Bloque por Bloque)

### 1. Configuración de Entorno e Inteligencia (Bloque 1)

* **Propósito:** Inicializar el motor de IA.
* **Detalle:**
* `ChatGoogleGenerativeAI`: Configura el modelo **Gemini 2.5 Flash**. Se utiliza una **temperatura de 0.4** para que el agente sea creativo al persuadir pero preciso al diagnosticar fallas.
* `convert_system_message_to_human`: Asegura la compatibilidad del formato de mensajes con la API de Google.



### 2. Base de Conocimientos (RAG) (Bloque 2)

* **Propósito:** Proporcionar "memoria técnica" al agente para evitar que invente información.
* **Detalle:**
* `documentos_soporte`: Matriz de conocimiento que incluye soluciones para la **Luz Roja (LOS)**, problemas de velocidad (frecuencia 5GHz) y **beneficios económicos** (15% de descuento, Plan Flex).
* `GoogleGenerativeAIEmbeddings`: Convierte el texto en vectores numéricos (`gemini-embedding-001`).
* `DocArrayInMemorySearch`: Almacena estos vectores para realizar búsquedas semánticas ultrarrápidas.



### 3. Herramientas de Acción (Tools) (Bloque 3)

* **Propósito:** Definir las capacidades operativas del agente.
* **Detalle:**
* `ClasificadorDeRiesgo`: Analiza el léxico del cliente. Si detecta palabras como "cancelar" o "competencia", dispara una alerta de riesgo alto.
* `BusquedaDeBeneficiosYSoluciones`: Conecta el razonamiento del agente con la base RAG del Bloque 2.
* `AgendarVisita` **(Plus)**: Función que simula la creación de una orden técnica en el sistema de Netlife si los pasos básicos fallan.
* `GenerarReporteTraspaso` **(Plus)**: Utiliza el resumen de la memoria para crear un ticket de escalamiento hacia un supervisor humano.



### 4. Memoria y Personalidad (Bloque 4)

* **Propósito:** Gestionar el hilo de la conversación y el comportamiento.
* **Detalle:**
* `ConversationSummaryMemory`: A diferencia de la memoria estándar, esta resume la charla continuamente. Esto permite que el agente "sepa" que el cliente estaba enojado hace 10 mensajes sin consumir demasiados tokens.
* `prefijo_agente`: Define el **System Prompt**. Establece las reglas de oro: ser empático, priorizar la retención y mencionar ubicaciones clave de **Guayaquil** (Mall del Sol, Ceibos) para generar confianza.



### 5. Interfaz de Ejecución (Bloque 5)

* **Propósito:** Mantener la sesión de chat activa.
* **Detalle:**
* `while True`: Bucle infinito que permite una conversación de ida y vuelta.
* `agente_netlife.invoke`: Punto de entrada único que procesa el texto, dispara las herramientas y devuelve la respuesta final.



---

## 🧪 Casos de Prueba Recomendados

| Entrada del Usuario | Comportamiento Esperado de la IA |
| --- | --- |
| "Mi internet está lento y es muy caro." | El agente debe detectar riesgo medio y ofrecer el **Plan Flex**. |
| "Tengo una luz roja en el módem." | El agente debe identificar rotura de fibra y ejecutar `AgendarVisita`. |
| "Me voy a cambiar a Claro, ellos me dan mejor precio." | El agente debe usar `ComparadorCompetencia` y ofrecer el **15% de descuento**. |

---

## ⚙️ Requisitos de Instalación

```bash
pip install langchain langchain-community langchain-google-genai chromadb docarray tiktoken sentence-transformers

```

> **Nota:** Se requiere una `GOOGLE_API_KEY` válida configurada como variable de entorno para la ejecución del modelo Gemini.

---
