# tests/test_main.py — comprueba que la API rechaza peticiones mal formadas

from fastapi.testclient import TestClient  # cliente de pruebas: llama a tu API sin levantarla

from app.main import app  # importa la aplicación que definiste

client = TestClient(app)  # con este cliente harás las peticiones de prueba


def test_chat_valida_entrada():  # pytest ejecuta toda función que empiece por test_
    r = client.post("/chat", json={})  # envía un JSON vacío: falta el campo "pregunta"
    assert r.status_code == 422  # 422 = Pydantic rechazó la entrada. No hace falta Ollama