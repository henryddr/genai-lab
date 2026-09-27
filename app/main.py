# app/main.py — API de chat que le pregunta a un modelo local con Ollama

import os  # para leer variables de entorno (lo que viene del archivo .env)

import httpx  # cliente HTTP asíncrono: con él tu API le habla a Ollama
from dotenv import load_dotenv  # carga el archivo .env
from fastapi import FastAPI  # el framework donde defines las rutas
from pydantic import BaseModel  # valida los datos que entran y salen

load_dotenv()  # lee .env; desde aquí sus valores están disponibles

# os.getenv(clave, respaldo): si la variable no existe, usa el segundo valor
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # dónde escucha Ollama
MODELO = os.getenv("OLLAMA_MODEL", "llama3.2")  # qué modelo usar, sin tocar el código

app = FastAPI(title="genai-lab")  # la aplicación; es la variable que busca uvicorn


class Pregunta(BaseModel):
    """Forma que debe tener el JSON que llega. Si no cumple, FastAPI responde 422."""

    pregunta: str  # campo obligatorio, de tipo texto


class Respuesta(BaseModel):
    """Forma del JSON que devuelves. Documenta la API y evita responder cualquier cosa."""

    respuesta: str  # el texto que generó el modelo
    modelo: str  # cuál lo generó: útil cuando compares modelos


# Ruta POST /chat. response_model hace que la salida se valide y se documente en /docs
@app.post("/chat", response_model=Respuesta)
# async: mientras espera al modelo, el servidor puede atender a otras personas
async def chat(req: Pregunta) -> Respuesta:
    # "async with" abre el cliente y lo cierra solo al salir del bloque
    async with httpx.AsyncClient(timeout=120) as client:  # 120 s: cargar el modelo tarda
        r = await client.post(  # await: espera aquí, pero deja correr otras tareas
            f"{OLLAMA_URL}/api/chat",  # el endpoint de chat de Ollama
            json={
                "model": MODELO,  # qué modelo debe responder
                # messages es una lista: el modelo no recuerda nada entre llamadas,
                # así que todo lo que deba saber viaja aquí, en cada petición
                "messages": [{"role": "user", "content": req.pregunta}],
                "stream": False,  # False: respuesta completa de una vez
            },
        )
        r.raise_for_status()  # si Ollama respondió con error (404, 500…), corta aquí
    # Ollama devuelve el texto en message.content; lo envolvemos en tu modelo de salida
    return Respuesta(respuesta=r.json()["message"]["content"], modelo=MODELO)