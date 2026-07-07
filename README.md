<div align="center">

# ✦ AETHER

### Cognitive Architecture Framework

**Transform frontier AI models into adaptive, self-improving cognitive systems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-7C6BFF.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org/)
[![Tauri](https://img.shields.io/badge/Tauri-2.x-FFC131.svg)](https://tauri.app/)

*The closest thing to AGI on your desktop.*

---

</div>

## What is Aether?

Aether is a premium open-source framework and desktop application that takes existing frontier models — Claude, Ollama, and other providers — and enhances them with a novel cognitive architecture layer featuring:

- **🧠 Dynamic Reasoning Engine (Cortex)** — Adaptive computation graphs where reasoning pathways form, strengthen, and prune based on task performance, inspired by neuroplasticity
- **🔬 Information-Geometric Metrics** — Reasoning quality measured via integrated information (Φ), Fisher information, and causal coherence
- **🧬 Safe Self-Improvement Loops** — Evaluate → Mutate → Select → Version reasoning strategies with built-in safety constraints and human-in-the-loop checkpoints
- **✨ Premium Desktop Experience** — A UI that feels like it was designed by Apple, with the warmth of Claude Desktop

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Tauri Desktop Shell                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              React + Vite Frontend                     │  │
│  │    Premium Dark UI • Framer Motion • Zustand          │  │
│  └───────────────────────┬───────────────────────────────┘  │
│                          │ Tauri Commands + HTTP             │
│  ┌───────────────────────▼───────────────────────────────┐  │
│  │           Python Cognitive Engine (FastAPI)             │  │
│  │                                                        │  │
│  │   ┌─────────┐  ┌─────────┐  ┌──────────────────┐     │  │
│  │   │ Cortex  │  │  Meta   │  │   Self-Improve   │     │  │
│  │   │ Dynamic │  │Cognitive│  │   Evaluate →      │     │  │
│  │   │Reasoning│  │ Monitor │  │   Mutate →        │     │  │
│  │   │  Graph  │  │         │  │   Select          │     │  │
│  │   └────┬────┘  └────┬────┘  └────────┬─────────┘     │  │
│  │        └─────────────┼───────────────┘                │  │
│  │                      ▼                                 │  │
│  │   ┌──────────────────────────────────────────────┐    │  │
│  │   │           Provider Registry                    │    │  │
│  │   │    Claude API  •  Ollama  •  Custom           │    │  │
│  │   └──────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- [Node.js](https://nodejs.org/) 20+
- [Rust](https://rustup.rs/) (latest stable)
- [Python](https://www.python.org/) 3.11+
- [Ollama](https://ollama.ai/) (optional — auto-detected if installed)

### 1. Clone & Install

```bash
git clone https://github.com/your-org/aether.git
cd aether

# Install frontend dependencies
npm install

# Install Python engine dependencies
cd engine
pip install -r requirements.txt
cd ..
```

### 2. Configure

```bash
# Set your Claude API key (or configure in Settings UI)
cp engine/.env.example engine/.env
# Edit engine/.env and add: AETHER_ANTHROPIC_API_KEY=your-key-here
```

### 3. Run

```bash
# Terminal 1: Start the cognitive engine
npm run engine

# Terminal 2: Start the desktop app
npm run tauri:dev
```

The app opens automatically. If Ollama is running locally, its models are auto-detected.

## Tech Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| Desktop Shell | **Tauri 2** (Rust) | Native window, tiny binary, system integration |
| Frontend | **React 19** + Vite + TypeScript | Fast, type-safe UI |
| Design | **Tailwind CSS** + Framer Motion | Premium dark theme with smooth animations |
| State | **Zustand** + TanStack Query | Lightweight state + async data management |
| Engine | **Python** + FastAPI | Cognitive architecture, ML ecosystem access |
| Providers | Anthropic SDK + httpx | Claude API + Ollama connectivity |

## Project Structure

```
aether/
├── src/                    # React frontend
│   ├── components/         #   Shared UI components
│   ├── features/           #   Feature modules (playground, models, etc.)
│   ├── hooks/              #   Custom React hooks
│   ├── lib/                #   Utilities, stores, API client
│   └── styles/             #   Design system tokens + animations
├── src-tauri/              # Rust backend (Tauri)
│   ├── src/commands/       #   IPC command handlers
│   └── capabilities/       #   Security permissions
├── engine/                 # Python cognitive engine
│   └── aether/
│       ├── providers/      #   Model providers (Claude, Ollama)
│       ├── cortex/         #   Dynamic reasoning engine
│       ├── metacognition/  #   Self-observation layer
│       ├── evolution/      #   Self-improvement system
│       └── api/            #   FastAPI endpoints
└── docs/                   # Documentation
```

## Development Roadmap

- [x] **Phase 1:** Foundation + Premium UI + Model Connectivity
- [ ] **Phase 2:** Dynamic Reasoning Engine (Cortex)
- [ ] **Phase 3:** Meta-Cognitive Monitoring Layer
- [ ] **Phase 4:** Self-Improvement Loop with Safety
- [ ] **Phase 5:** Experiment Playground + Polish

## Design Philosophy

Aether's design language is **"Calm Power"** — a fusion of Claude Desktop's warmth with Apple's spatial precision. Every surface communicates depth through subtle luminosity shifts. The color palette centers on electric violet (#7C6BFF) against near-black surfaces, with teal and coral accents for data visualization and alerts.

## Contributing

Contributions are welcome. Please read the docs and follow the existing code style.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with obsessive attention to detail.**

*Aether — Think beyond.*

</div>
