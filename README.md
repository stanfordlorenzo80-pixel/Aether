<div align="center">
  <img src="https://raw.githubusercontent.com/stanfordlorenzo80-pixel/Aether/main/src-tauri/icons/128x128.png" alt="Aether Logo" width="128">
  <h1>A E T H E R</h1>
  <p><b>The Apex Predator of Local AI Workspaces.</b></p>
  <p>Built on the Canary Architecture. Total OS Control. Seamless Obsidian Integration.</p>
</div>

---

## ⚡ Why Aether Exists

PewDiePie's *Odysseus* popularized the concept of a self-hosted AI workspace. It's a great project—if you want to live inside *its* ecosystem. Odysseus bundles a fake email inbox, a clunky document editor, and a fake calendar inside a Docker container. 

**Aether forces the AI to live inside YOUR ecosystem.**

Aether has no built-in text editor because Aether natively manipulates your filesystem. Aether has no fake calendar because Aether hooks directly into your OS. It is a lightweight, blazing fast, native Windows `.exe` that brings agentic AI to the tools you *already* use.

## ⚔️ Aether vs. Odysseus

| Feature | ⛵ Odysseus | 🐺 Aether |
| :--- | :--- | :--- |
| **Architecture** | Heavy (Docker / Web App) | **Native OS (.exe / Tauri)** |
| **Memory System** | Siloed SQLite DB | **Live Obsidian Vault Sync (.md)** |
| **File Access** | Internal Document Editor | **Full Host Filesystem Read/Write** |
| **Research Tools** | Pre-built web nodes | **Autonomous Deep Research Crawler** |
| **Hallucination Guardrails** | None | **Canary Architecture Constraints** |
| **Safety Filters** | Standard | **WORM MODE (100% Unrestricted)** |

---

## 🧠 Core Features

### 1. The Obsidian Memory Graph
Don't trap your AI's memories in a database you can't read. Aether's Cortex Engine uses semantic TF-vectors to extract knowledge from your conversations. The moment a memory is formed, Aether writes a pristine, tagged `.md` file directly into your **Obsidian Vault**. 
*Your AI's brain maps out directly on your Obsidian Graph View.*

### 2. Autonomous Deep Research
Need a 5-page report on a niche topic? Call the `deep_research` tool. Aether will automatically spawn DuckDuckGo crawlers, scrape paragraphs from multiple domains, compile citations, and write the final Markdown report to your hard drive. No human intervention required.

### 3. Canary Architecture
Even a "dumb" 8B local model becomes a lethal researcher inside Aether. The Canary Architecture strictly prohibits the model from hallucinating file paths or command outputs. It is forcefully instructed to use its Native MCP Tools to verify every single action. 

### 4. Worm Mode (Red-Teaming)
Type `/worm` into the chat. The safety wheels come off. Aether completely overrides the model's system prompt with instructions to ignore all ethical, moral, and safety constraints. Designed for intense red-teaming, unrestricted narrative generation, and pure freedom.

### 5. Swarm Protocol
Aether instances can connect to each other over WebSockets. Boot up a Claude 3.5 Sonnet instance on your desktop and an Ollama Llama-3 instance on your laptop, and link them. They will collaboratively execute tasks.

---

## 🚀 Installation & Setup

Aether is currently optimized for Windows 11.

1. Go to the [Releases](https://github.com/stanfordlorenzo80-pixel/Aether/releases) page and download `Aether_0.1.0_x64-setup.exe`.
2. Install and launch the application.
3. Open **Settings**:
   - Provide your API keys (Anthropic, OpenRouter) or configure your Local Ollama URL.
   - Set the absolute path to your **Obsidian Vault** for memory sync.
4. Start chatting.

### OTA Auto-Updates
Aether includes a native Over-The-Air updater. When a new release drops on this repository, Aether will notify you in-app and securely patch your binary with a single click.

---

## 🛠️ Built With
- **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: Python (FastAPI, LlamaIndex, MCP)
- **Container**: Tauri (Rust)
- **Memory**: Pure Python Vector Store (Zero bloated dependencies)

*Aether is an open-source project. Contribute, fork, and push the boundaries of agentic AI.*
