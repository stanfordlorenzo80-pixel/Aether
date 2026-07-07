"""Aether Engine configuration via environment variables and .env file."""

import os

class AetherConfig:
    """Central configuration for the Aether cognitive engine.

    All values can be overridden via environment variables prefixed with AETHER_.
    """
    def __init__(self):
        # ── Server ──────────────────────────────────────────────────────────────
        self.host = os.environ.get("AETHER_HOST", "0.0.0.0")
        self.port = int(os.environ.get("AETHER_PORT", "8420"))
        self.debug = os.environ.get("AETHER_DEBUG", "false").lower() == "true"
        
        # ── Provider: Anthropic (Claude) ────────────────────────────────────────
        self.anthropic_api_key = os.environ.get("AETHER_ANTHROPIC_API_KEY", "")
        
        # ── Provider: Ollama (local) ────────────────────────────────────────────
        self.ollama_base_url = os.environ.get("AETHER_OLLAMA_BASE_URL", "http://localhost:11434")
        
        # ── Engine Defaults ─────────────────────────────────────────────────────
        self.default_provider = os.environ.get("AETHER_DEFAULT_PROVIDER", "claude")
        self.default_model = os.environ.get("AETHER_DEFAULT_MODEL", "claude-sonnet-4-20250514")
        self.max_tokens = int(os.environ.get("AETHER_MAX_TOKENS", "4096"))
        self.temperature = float(os.environ.get("AETHER_TEMPERATURE", "0.7"))

# Module-level singleton — import `config` from anywhere.
config = AetherConfig()
