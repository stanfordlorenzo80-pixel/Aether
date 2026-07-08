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

# ── Health ───────────────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    providers = registry.list_providers()
    return {
        "status": "ok",
        "running": True,
        "version": "0.1.0",
        "uptime": 0, 
        "providers": [p["id"] for p in providers],
        "swarm_peers": len(swarm.peers),
        "memories": len(memory_store.memories)
    }

# ── Models & Providers ───────────────────────────────────────────────────────

@app.get("/api/models/providers")
async def list_providers():
    """Returns providers with nested models — matches frontend ProviderInfo shape."""
    return registry.list_providers()

@app.get("/api/models")
async def list_models():
    """Flat list of all models across all providers."""
    return await registry.list_all_models()

@app.post("/api/models/test/{provider_id}")
async def test_provider(provider_id: str):
    provider = registry.get_provider(provider_id)
    if not provider:
        return {"connected": False, "latency": 0, "error": "Provider not found"}
    status = await provider.test_connection()
    return {"connected": status[0], "latency": status[1], "error": status[2]}

@app.post("/api/providers/refresh/{provider_id}")
async def refresh_provider(provider_id: str):
    """Re-initialize and re-test a single provider (e.g., after key change)."""
    result = await registry.refresh_provider(provider_id)
    return result

@app.post("/api/providers/refresh")
async def refresh_all_providers():
    """Re-initialize all providers."""
    results = {}
    for name in ["claude", "ollama", "openrouter"]:
        results[name] = await registry.refresh_provider(name)
    return results

# ── Settings ─────────────────────────────────────────────────────────────────

@app.post("/api/settings/api-key")
async def save_api_key(request: Request):
    """Save an API key for a provider and immediately refresh it."""
    body = await request.json()
    provider_name = body.get("provider", "")
    api_key = body.get("key", "")
    
    if not provider_name:
        return {"success": False, "error": "Provider name required"}
    
    updated = registry.update_api_key(provider_name, api_key)
    if not updated:
        return {"success": False, "error": f"Provider '{provider_name}' not found or doesn't support API keys"}
    
    # Immediately test the new key
    result = await registry.refresh_provider(provider_name)
    return {"success": True, **result}

@app.post("/api/settings/ollama-url")
async def save_ollama_url(request: Request):
    """Update the Ollama base URL and re-probe."""
    body = await request.json()
    url = body.get("url", "")
    
    if not url:
        return {"success": False, "error": "URL required"}
    
    registry.update_ollama_url(url)
    result = await registry.refresh_provider("ollama")
    return {"success": True, **result}

# ── Swarm ────────────────────────────────────────────────────────────────────

@app.post("/api/swarm/connect")
async def connect_peer(request: Request):
    body = await request.json()
    peer_url = body.get("url")
    if not peer_url:
        return {"error": "url required"}
    peers = swarm.connect(peer_url)
    return {"connected": True, "peers": peers}

# ── Chat ─────────────────────────────────────────────────────────────────────

@app.post("/api/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    model_id = body.get("model")
    stream = body.get("stream", False)
    
    provider = registry.resolve_provider_for_model(model_id)
    if not provider:
        provider = registry.get_provider("ollama") or registry.get_provider("claude") or registry.get_provider("openrouter")
    
    if not provider:
        return {"error": "No providers available"}
            
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
        try:
            result = await provider.chat(model_id, messages)
            return {"choices": [{"message": {"content": result}}]}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8420)
