<div align="center">
  <h1>🌌 Aether</h1>
  <p><strong>A Next-Generation, Distributed Cognitive Architecture & P2P AI Engine</strong></p>

  <p>
    <img src="https://img.shields.io/badge/version-v0.1.0-blue.svg?style=for-the-badge" alt="Version">
    <img src="https://img.shields.io/badge/build-passing-brightgreen.svg?style=for-the-badge" alt="Build">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" alt="License">
  </p>
</div>

---

## What is Aether?

Aether is a full-stack, distributed **Cognitive Architecture** built on a native Rust/Tauri desktop shell with a standalone Python engine. It dynamically routes reasoning tasks across cloud providers (Claude, OpenRouter) and local hardware (Ollama), stores long-term memory in a local vector database, and uses a P2P Swarm network to distribute compute across multiple machines.

## ⚡ Key Features

* **Multi-Provider Model Access**: Seamlessly connect to Anthropic Claude, OpenRouter (100+ models including Llama, Mixtral, Command R+), and local Ollama models — all from a single interface.
* **Hot-Swap API Keys**: Add or change API keys directly in the Settings UI. The engine instantly re-authenticates without restart.
* **Neuroplastic Routing Graph**: Automatically analyzes prompts and routes them to the optimal LLM based on task complexity, context length, and required capabilities.
* **Long-Term Vector Memory**: Automatically persists conversation history into a local TF-IDF vector store and injects relevant context into future prompts.
* **P2P Swarm Mesh**: Connect multiple Aether nodes across a network via WebSockets to distribute heavy reasoning tasks.
* **Zero-Friction Standalone EXE**: The entire Python cognitive engine is frozen via PyInstaller into a hidden "Sidecar". When you run `Aether.exe`, everything boots up seamlessly.
* **OTA Auto-Updates**: Built-in Rust-native auto-updater. New releases are downloaded and installed directly within the app.

## 🚀 Installation

Aether is compiled as a standalone installer for Windows. No Python environments or dependencies required.

1. Head to the [Releases](https://github.com/stanfordlorenzo80-pixel/Aether/releases) tab and download the latest `Aether_x64-setup.exe` or `Aether_x64_en-US.msi`.
2. Run the installer.
3. Open Aether. The engine sidecar auto-launches on port `8420`.
4. Go to **Settings** → add your API keys (Anthropic, OpenRouter) or configure your Ollama URL.
5. Go to **Models** → see all available models, select one, and start chatting.

## 🔌 Headless Plugin / API Mode

Aether's engine runs as a local FastAPI server on port `8420`. Any local script, browser extension, or IDE plugin can hit the API:

```bash
# Health check
curl http://127.0.0.1:8420/health

# List all providers with models
curl http://127.0.0.1:8420/api/models/providers

# List all models (flat)
curl http://127.0.0.1:8420/api/models

# Chat completion (streaming)
curl -X POST http://127.0.0.1:8420/api/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","messages":[{"role":"user","content":"hello"}],"stream":true}'

# Save API key at runtime
curl -X POST http://127.0.0.1:8420/api/settings/api-key \
  -H "Content-Type: application/json" \
  -d '{"provider":"claude","key":"sk-ant-..."}'

# Test a provider connection
curl -X POST http://127.0.0.1:8420/api/models/test/ollama
```

## 🛠️ Architecture

| Layer | Technology |
|---|---|
| Desktop Shell | Tauri 2.0 (Rust) |
| Frontend | React 18, Vite, Vanilla CSS, Framer Motion |
| Cognitive Engine | Python 3.11, FastAPI, Uvicorn |
| Providers | Anthropic SDK, OpenRouter API, Ollama REST |
| Memory Store | Local Vector Embeddings (TF-IDF / Cosine Similarity) |
| Networking | aiohttp WebSocket Mesh |
| Packaging | PyInstaller (engine), NSIS/MSI (installer) |

## 📜 License

This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
