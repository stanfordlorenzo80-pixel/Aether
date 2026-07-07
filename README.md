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

Aether is not just another LLM wrapper—it is a full-stack, distributed **Cognitive Architecture**. Built on a native Rust/Tauri desktop shell with a standalone Python engine, Aether dynamically routes reasoning tasks across cloud providers (Claude, OpenAI) and local hardware (Ollama), stores long-term memory in a local vector database, and uses a P2P Swarm network to distribute compute across multiple machines.

## ⚡ Key Features

* **Neuroplastic Routing Graph**: Automatically analyzes prompts and routes them to the optimal LLM based on task complexity, context length, and required capabilities.
* **Long-Term Vector Memory**: Aether automatically persists conversation history into a local TF-IDF vector store and injects relevant context into future prompts organically.
* **P2P Swarm Mesh**: Connect multiple Aether nodes across a network via WebSockets to distribute heavy reasoning tasks and establish an autonomous multi-agent swarm.
* **Zero-Friction Standalone EXE**: The entire Python cognitive engine is frozen via PyInstaller into a hidden "Sidecar". When you run `Aether.exe`, everything boots up seamlessly. No terminal windows required.
* **OTA Auto-Updates**: Built-in Rust-native auto-updater. When a new release drops on GitHub, Aether downloads and installs it directly within the app.

## 🚀 Installation (One-Click Launch)

Aether is compiled as a standalone `.exe` for Windows. There are no Python virtual environments to set up and no dependencies to install. 

1. Head to the [Releases](#) tab and download the latest `Aether.msi` or `Aether.exe`.
2. Double-click the installer.
3. Open the app and drop your Anthropic API Key or hook up your local Ollama instance in the **Settings** menu.

## 🔌 Headless Plugin / API Mode

Because Aether's core runs as a local FastAPI sidecar on port `8420`, the entire cognitive architecture can be leveraged as a plugin. 

Any local script, Chrome Extension, or IDE plugin can send an HTTP or WebSocket request to `http://127.0.0.1:8420/api/chat` to harness Aether's swarm and memory graph completely headless.

## 🛠️ Architecture Stack

- **Desktop Shell**: Tauri 2.0 (Rust)
- **Frontend**: React, Vite, Tailwind CSS, Framer Motion
- **Cognitive Engine**: Python 3.11, FastAPI, DSPy
- **Memory Store**: Local Vector Embeddings (TF-IDF/Cosine Similarity)
- **Networking**: `aiohttp` WebSocket Mesh

## 📜 License

This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
