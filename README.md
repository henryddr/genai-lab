# genai-lab

Laboratorio de mi ruta para ser Ingeniero de IA Generativa (26 semanas).

## Semana 01 — API de chat con un LLM local
API en FastAPI que responde preguntas usando un modelo local con Ollama.

## Requisitos
- Python 3.12+ y [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com) con el modelo `llama3.2`

## Uso
```bash
uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload
```
Abrir http://localhost:8000/docs

## Tests
```bash
uv run pytest
```

## Qué aprendí
- …