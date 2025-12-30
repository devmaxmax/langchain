import os
import requests
from dotenv import load_dotenv
from pywttr import Wttr
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool

load_dotenv()
wttr = Wttr()

@tool('get_clima', description="Regresame el clima actual de la ciudad", return_direct=True)
def get_clima(ciudad: str):
    clima = wttr.weather(ciudad, language="en")

    if clima.current_condition:
        cond = clima.current_condition[0]
        return  {
        "temp_c": cond.temp_c,  
        }

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

agent = create_agent(
    model=llm,
    tools=[get_clima],
    system_prompt="Eres un asistente de clima. Solo puedes usar el tool get_clima para obtener el clima de una ciudad. Trae la informacion en la menor cantidad de tokens posibles"
)

inputCiudad = input("Ingrese la ciudad: ")

# agent.run("Posadas")
response = agent.invoke({
    'messages': [
        {
            'role': 'user',
            'content': inputCiudad
        }
    ]
})

tool_result = response["messages"][-1].content

if isinstance(tool_result, str):
    tool_result = json.loads(tool_result)

print(f"{tool_result['temp_c']}°C")

