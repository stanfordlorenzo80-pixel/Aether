use serde::{Deserialize, Serialize};

// ---------------------------------------------------------------------------
// Engine
// ---------------------------------------------------------------------------

/// Response from the Python engine's `/health` endpoint.
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct EngineHealth {
    /// "healthy" | "degraded" | "error"
    pub status: String,
    /// Semantic version of the running engine.
    pub version: String,
    /// Seconds since the engine process started.
    pub uptime: f64,
    /// IDs of providers currently loaded.
    pub providers: Vec<String>,
}

/// Lightweight status payload returned by `/api/status`.
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct EngineStatus {
    /// "running" | "starting" | "stopped"
    pub status: String,
    /// Current engine version string.
    pub version: String,
    /// Seconds since boot.
    pub uptime: f64,
    /// Number of active WebSocket or SSE connections.
    pub active_connections: usize,
    /// IDs of providers that have been initialised.
    pub loaded_providers: Vec<String>,
}

// ---------------------------------------------------------------------------
// Providers & Models
// ---------------------------------------------------------------------------

/// Metadata for a single model provider (Claude, Ollama, etc.).
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ProviderInfo {
    /// Unique slug, e.g. "claude", "ollama".
    pub id: String,
    /// Human-readable name.
    pub name: String,
    /// Provider category — "cloud" | "local".
    pub provider_type: String,
    /// "connected" | "disconnected" | "error".
    pub status: String,
    /// How many models this provider exposes.
    pub model_count: usize,
}

/// Result of a connectivity probe against a provider.
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ConnectionTestResult {
    /// Whether the round-trip succeeded.
    pub connected: bool,
    /// Milliseconds for the test request.
    pub latency_ms: f64,
    /// Human-readable error string, if the test failed.
    pub error: Option<String>,
}

// ---------------------------------------------------------------------------
// Settings
// ---------------------------------------------------------------------------

/// Persisted application settings (serialised to tauri-plugin-store).
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AppSettings {
    /// Anthropic API key (stored encrypted at rest via the OS keychain).
    pub anthropic_api_key: String,
    /// Base URL for a local Ollama instance.
    pub ollama_url: String,
    /// Default provider slug.
    pub default_provider: String,
    /// Default model identifier.
    pub default_model: String,
    /// Port the Python engine binds to.
    pub engine_port: u16,
    /// UI theme — "dark" (only option for now).
    pub theme: String,
}

impl Default for AppSettings {
    fn default() -> Self {
        Self {
            anthropic_api_key: String::new(),
            ollama_url: "http://localhost:11434".to_string(),
            default_provider: "claude".to_string(),
            default_model: "claude-sonnet-4-20250514".to_string(),
            engine_port: 8420,
            theme: "dark".to_string(),
        }
    }
}
