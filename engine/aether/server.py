import asyncio
import json
from typing import AsyncGenerator
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from aether.memory import LocalVectorStore
from aether.swarm import AetherSwarm
from aether.providers.registry import ProviderRegistry

app = FastAPI(title="Aether Engine", version="0.1.0")
registry = ProviderRegistry()
memory_store = LocalVectorStore()
swarm = AetherSwarm()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await registry.initialize()

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "running": True,
        "version": "0.1.0",
        "uptime": 0, 
        "providers": [p["name"] for p in registry.list_providers()],
        "swarm_peers": len(swarm.peers),
        "memories": len(memory_store.memories)
    }

@app.get("/api/models/providers")
async def list_providers():
    return registry.list_providers()

@app.get("/api/models")
async def list_models():
    models = await registry.list_all_models()
    return [{"id": m.id, "name": m.name, "provider": m.provider} for m in models]

@app.post("/api/swarm/connect")
async def connect_peer(request: Request):
    body = await request.json()
    peer_url = body.get("url")
    if not peer_url:
        return {"error": "url required"}
    peers = swarm.connect(peer_url)
    return {"connected": True, "peers": peers}

@app.post("/api/models/test/{provider_id}")
async def test_provider(provider_id: str):
    provider = registry.get_provider(provider_id)
    if not provider:
        return {"connected": False, "latency": 0, "error": "Not found"}
    status = await provider.test_connection()
    return {"connected": status.connected, "latency": status.latency_ms, "error": status.error}

@app.post("/api/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    model_id = body.get("model")
    stream = body.get("stream", False)
    
    provider = registry.resolve_provider_for_model(model_id)
    if not provider:
        provider = registry.get_provider("claude") or registry.get_provider("openrouter") or registry.get_provider("ollama")
            
    if messages:
        last_msg = messages[-1].get("content", "")
        if last_msg:
            memory_store.store_episode(last_msg, {"model": model_id})
            
    if stream:
        async def event_generator() -> AsyncGenerator[str, None]:
            try:
                async for chunk in provider.stream_chat(model_id, messages):
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk})}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        return {"choices": [{"message": {"content": "Non-streaming not fully implemented yet."}}]}

if __name__ == "__main__":
    uvicorn.run("aether.server:app", host="127.0.0.1", port=8420, reload=True)
