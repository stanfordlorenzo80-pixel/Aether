import asyncio
import json
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from aether.registry import ModelRegistry

app = FastAPI(title="Aether Engine", version="0.1.0")
registry = ModelRegistry()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Registry auto-initializes and detects Ollama in background
    await registry.initialize()

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "running": True,
        "version": "0.1.0",
        "uptime": 0, # Add uptime tracking later
        "providers": list(registry.providers.keys())
    }

@app.get("/api/models/providers")
async def list_providers():
    return registry.get_all_providers_info()

@app.post("/api/models/test/{provider_id}")
async def test_provider(provider_id: string):
    success, latency, err = await registry.test_connection(provider_id)
    return {"connected": success, "latency": latency, "error": err}

@app.post("/api/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    model_id = body.get("model")
    stream = body.get("stream", False)
    
    # Simple parse to find the provider
    provider_id = "claude" # default
    for pid, provider in registry.providers.items():
        if any(m.id == model_id for m in provider.models):
            provider_id = pid
            break
            
    if stream:
        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                async for chunk in registry.stream_chat(provider_id, model_id, messages):
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        # Non-streaming fallback
        pass

if __name__ == "__main__":
    uvicorn.run("aether.server:app", host="127.0.0.1", port=8420, reload=True)
