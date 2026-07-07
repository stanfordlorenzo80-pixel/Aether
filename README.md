<div align="center">
  <h1>🌌 Aether</h1>
  <p><strong>The Next Step in AI Evolution: A Dynamic, Self-Improving Cognitive Architecture</strong></p>

  <p>
    <a href="https://github.com/stanfordlorenzo80-pixel/Aether/releases"><img src="https://img.shields.io/github/v/release/stanfordlorenzo80-pixel/Aether" alt="Release"></a>
    <a href="https://github.com/stanfordlorenzo80-pixel/Aether/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
    <a href="https://github.com/stanfordlorenzo80-pixel/Aether/issues"><img src="https://img.shields.io/github/issues/stanfordlorenzo80-pixel/Aether" alt="Issues"></a>
  </p>
</div>

---

Aether is a premium, open-source AI desktop application and framework that advances the capabilities of frontier models (Claude, Ollama, OpenAI) by wrapping them in a **dynamic reasoning graph** and an **autonomous self-improvement loop**. 

It’s designed to be the closest thing to AGI you can run locally, combining a stunning Apple-grade desktop UI (built with Tauri and React) with a cutting-edge Python cognitive engine.

## 🧠 Core Architecture

Aether abandons static prompt chains in favor of a fluid, neuroplasticity-inspired architecture. 

### 1. The Cortex (Dynamic Reasoning DAG)
Instead of feeding your prompt blindly to an LLM, the **Adaptive Router** (powered by a fast classification LLM) analyzes the intent and constructs a directed acyclic graph (DAG) of reasoning pathways in real-time.
- **Analytical Node**: Demands strict, formal logic and step-by-step breakdowns.
- **Creative Node**: Injects divergent thinking and lateral associations.
*Pathways strengthen or prune themselves based on historical success.*

### 2. Meta-Cognition (LLM-as-a-Judge)
Aether watches itself think. 
- **Performance Evaluator**: Scores output based on accuracy, depth, and logical coherence.
- **Phi Calculator**: Approximates Integrated Information Theory (IIT) by calculating the causal coherence and interdependency of the reasoning graph's nodes.

### 3. Evolution (DSPy-Style Programmatic Optimization)
Aether is capable of autonomous self-improvement. When the Meta-Cognitive layer detects an anomaly or a low-scoring reasoning trace, the **Mutation Engine** rewrites its own internal system prompts, benchmarks the variants locally, and permanently adopts the highest-performing neural weights.

---

## 💻 The Desktop Experience

Aether isn’t just a terminal tool. It ships with a beautiful, dark-mode-first desktop shell built on Tauri 2.x.
- **Calm Power Design**: Fluid Framer Motion animations, deeply tailored color palettes, and micro-interactions.
- **Seamless Provider Connectivity**: Built-in support for Anthropic Claude (Primary) and zero-config auto-detection for local Ollama models.
- **Real-Time Streaming**: Server-Sent Events (SSE) ensure zero-latency token streaming from the Python engine to the React frontend.

---

## 🚀 Quick Start

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Rust](https://rustup.rs/)
- [Python 3.10+](https://www.python.org/)
- Anthropic API Key (or Ollama installed locally)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/stanfordlorenzo80-pixel/Aether.git
   cd Aether
   ```

2. **Set up the Python Engine:**
   ```bash
   cd engine
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn anthropic networkx aiohttp
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Start the Engine:**
   ```bash
   python -m aether.server
   ```

4. **Launch the Desktop App:**
   In a new terminal window:
   ```bash
   npm install
   npm run tauri dev
   ```

---

## 🗺️ Roadmap
- [x] **Phase 1**: Tauri Desktop Shell & Python Engine Foundation
- [x] **Phase 2**: Cortex Graph & Dynamic LLM Routing
- [x] **Phase 3**: Meta-Cognitive Evaluator & Coherence Scoring
- [x] **Phase 4**: Evolutionary Self-Improvement Loop & Mutations
- [ ] **Phase 5**: Multi-modal memory embeddings & local vector store
- [ ] **Phase 6**: Distributed reasoning swarms across network peers

---

## 🤝 Contributing
Aether is an open-source initiative pushing the boundaries of autonomous cognitive architectures. We welcome PRs for new Reasoning Nodes, advanced Meta-Cognitive metrics, and UI refinements. 

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

---

<div align="center">
  <i>Think beyond.</i>
</div>
