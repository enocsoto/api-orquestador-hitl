import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


async def redactar(instruccion: str, datos: str) -> str:
    """Si hay clave, el modelo redacta. Si no, el dato de la herramienta sale tal cual."""
    if not os.getenv("OPENAI_API_KEY", "").strip():
        return datos
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    message = await model.ainvoke(
        [SystemMessage(content=instruccion), HumanMessage(content=datos)]
    )
    return str(message.content)
