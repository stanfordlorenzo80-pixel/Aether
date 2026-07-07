"""Chat completion endpoints — SSE streaming and model listing."""

from __future__ import annotations

import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from aether.providers.base import CompletionRequest, StreamChunk
from aether.providers.registry import ProviderRegistry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


# ── Helpers ─────────────────────────────────────────────────────────────────


async def _stream_completion(
    request: CompletionRequest,
) -> AsyncGenerator[dict, None]:
    """Resolve a provider and yield SSE-ready dicts from its completion stream."""
    registry = ProviderRegistry()

    # Resolve which provider handles this model.
    provider = registry.resolve_provider_for_model(request.model)
    if provider is None:
        yield {
            "event": "chunk",
            "data": StreamChunk(
                type="error",
                error="No provider available for the requested model",
            ).model_dump_json(),
        }
        yield {
            "event": "chunk",
            "data": StreamChunk(type="done").model_dump_json(),
        }
        return

    logger.info(
        "Streaming completion via %s (model=%s, msgs=%d)",
        provider.name,
        request.model or "default",
        len(request.messages),
    )

    try:
        async for chunk in provider.complete(request):
            yield {
                "event": "chunk",
                "data": chunk.model_dump_json(),
            }
    except Exception as exc:  # noqa: BLE001
        logger.exception("Stream error")
        yield {
            "event": "chunk",
            "data": StreamChunk(type="error", error=str(exc)).model_dump_json(),
        }
        yield {
            "event": "chunk",
            "data": StreamChunk(type="done").model_dump_json(),
        }


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.post("/completions")
async def create_completion(request: CompletionRequest) -> EventSourceResponse:
    """Stream a chat completion as Server-Sent Events.

    Each SSE event has ``event: chunk`` and a JSON ``data`` payload
    conforming to the ``StreamChunk`` schema.  The final event will
    have ``type: done``.

    **Example cURL**::

        curl -N -X POST http://localhost:8420/api/chat/completions \\
          -H 'Content-Type: application/json' \\
          -d '{"messages":[{"role":"user","content":"Hello"}]}'
    """
    if not request.messages:
        raise HTTPException(status_code=422, detail="messages list must not be empty")

    return EventSourceResponse(
        _stream_completion(request),
        media_type="text/event-stream",
    )


@router.get("/models")
async def list_chat_models() -> dict:
    """Return all models available for chat completions.

    Response::

        {
            "models": [ { ModelInfo fields } ],
            "default_model": "claude-sonnet-4-20250514"
        }
    """
    registry = ProviderRegistry()
    models = await registry.list_all_models()
    from aether.config import config as _cfg

    return {
        "models": [m.model_dump() for m in models],
        "default_model": _cfg.default_model,
    }
