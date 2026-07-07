"""Aether Engine configuration via environment variables and .env file."""

from pydantic import Field
from pydantic_settings import BaseSettings


class AetherConfig(BaseSettings):
    """Central configuration for the Aether cognitive engine.

    All values can be overridden via environment variables prefixed with AETHER_
    or via a .env file placed alongside the engine package.
    """

    # ── Server ──────────────────────────────────────────────────────────────
    host: str = Field(default="0.0.0.0", description="Bind address for the HTTP server")
    port: int = Field(default=8420, description="Port for the HTTP server")
    debug: bool = Field(default=False, description="Enable debug mode (verbose logging, auto-reload)")

    # ── Provider: Anthropic (Claude) ────────────────────────────────────────
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key — required for Claude provider",
    )

    # ── Provider: Ollama (local) ────────────────────────────────────────────
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Base URL for the local Ollama instance",
    )

    # ── Engine Defaults ─────────────────────────────────────────────────────
    default_provider: str = Field(
        default="claude",
        description="Default inference provider name",
    )
    default_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Default model identifier",
    )
    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=128_000,
        description="Default max output tokens per completion",
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Default sampling temperature",
    )

    model_config = {
        "env_prefix": "AETHER_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Module-level singleton — import `config` from anywhere.
config = AetherConfig()
