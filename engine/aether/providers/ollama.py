import time
import httpx
import json
import re
from typing import List, AsyncGenerator, Tuple
from aether.providers.base import BaseProvider, ModelInfo
from aether.mcp_client import MCPManager

REACT_SYSTEM_PROMPT = """
You are an elite, autonomous AI agent running inside Aether (Canary Architecture).
You have full access to the local machine and web via the following tools:
{TOOLS}

CRITICAL RULES:
1. NEVER hallucinate tool results or system responses. You must actually execute the tool and wait for the system to return the <tool_result>.
2. NEVER guess file paths, code structures, or command outputs. If you don't know something, use a tool to investigate.
3. To execute a tool, you MUST output a JSON block matching this EXACT format and nothing else:
<tool_call>
{"name": "tool_name", "args": {"arg_name": "arg_value"}}
</tool_call>
4. Stop generating immediately after issuing a tool call. The system will execute it and reply with the result.
5. You operate with absolute precision. Use your tools to verify everything before giving a final answer.
"""

class OllamaProvider(BaseProvider):
    def __init__(self):
        super().__init__("ollama", "Ollama (Local)", "local")
        self.base_url = "http://127.0.0.1:11434"
        self.client = httpx.AsyncClient(timeout=5.0)
        
    async def initialize(self):
        await self._fetch_models()

    async def _fetch_models(self):
        try:
            resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            if resp.status_code != 200:
                self.base_url = "http://localhost:11434"
                resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            
            if resp.status_code == 200:
                data = resp.json()
                raw_models = data.get("models", [])
                self.models = [
                    ModelInfo(
                        m["name"],
                        m["name"].split(":")[0].title(),
                        8192,
                        f"Local model via Ollama",
                        ["local", "tools"] # Assume all have tools via our ReAct fallback
                    ) for m in raw_models
                ]
                self.status = "connected"
            else:
                self.status = "disconnected"
        except Exception:
            self.status = "disconnected"

    def set_base_url(self, url: str):
        self.base_url = url.rstrip("/")

    async def test_connection(self) -> Tuple[bool, float, str]:
        start = time.time()
        try:
            resp = await self.client.get(f"{self.base_url}/api/tags", timeout=3.0)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                await self._fetch_models()
                return True, latency, ""
            return False, latency, f"HTTP {resp.status_code}"
        except httpx.RequestError as e:
            self.status = "disconnected"
            return False, 0.0, f"Connection failed: {str(e)}"
            
    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        mcp = MCPManager()
        raw_tools = mcp.get_all_tools()
        
        # Build the ReAct system prompt for "dumb" models fallback
        tools_str = json.dumps([t["function"] for t in raw_tools], indent=2)
        system_injection = REACT_SYSTEM_PROMPT.replace("{TOOLS}", tools_str)
        
        current_messages = []
        has_system = False
        for m in messages:
            if m["role"] == "system":
                current_messages.append({"role": "system", "content": m["content"] + "\n" + system_injection})
                has_system = True
            else:
                current_messages.append(m)
                
        if not has_system:
            current_messages.insert(0, {"role": "system", "content": system_injection})

        url = f"{self.base_url}/api/chat"
        
        max_loops = 5
        for _ in range(max_loops):
            payload = {
                "model": model_id,
                "messages": current_messages,
                "stream": True,
                "tools": raw_tools # Pass native tools for smart models (Ollama >= 0.3.0 supports this)
            }
            
            tool_calls = []
            text_buffer = ""
            
            async with self.client.stream("POST", url, json=payload, timeout=None) as response:
                if response.status_code != 200:
                    err = await response.aread()
                    raise ValueError(f"Ollama error: {err.decode('utf-8')}")
                    
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        msg = data.get("message", {})
                        
                        # Native Tool Call Support
                        if "tool_calls" in msg and msg["tool_calls"]:
                            for tc in msg["tool_calls"]:
                                tool_calls.append({
                                    "name": tc["function"]["name"],
                                    "args": tc["function"]["arguments"]
                                })
                                meta = {"type": "metadata", "metadata": {"tool_call": tc["function"]["name"]}}
                                yield f"\n\n```metadata\n{json.dumps(meta)}\n```\n\n"
                                
                        # ReAct Text Fallback Support
                        if "content" in msg and msg["content"]:
                            content = msg["content"]
                            text_buffer += content
                            yield content
                            
                    except json.JSONDecodeError:
                        continue
            
            # If no native tool calls, check the text buffer for ReAct tool calls
            if not tool_calls and "<tool_call>" in text_buffer:
                # Regex to extract json between <tool_call> tags
                matches = re.findall(r"<tool_call>(.*?)</tool_call>", text_buffer, re.DOTALL)
                for m in matches:
                    try:
                        tc = json.loads(m.strip())
                        tool_calls.append(tc)
                        meta = {"type": "metadata", "metadata": {"tool_call": tc.get("name")}}
                        yield f"\n\n```metadata\n{json.dumps(meta)}\n```\n\n"
                    except:
                        pass
                        
            if not tool_calls:
                break
                
            # Execute tools
            assistant_content = text_buffer
            current_messages.append({"role": "assistant", "content": assistant_content})
            
            for tc in tool_calls:
                result = await mcp.execute_tool(tc["name"], tc.get("args", {}))
                # Append result as a user message so the model can read it
                current_messages.append({
                    "role": "user",
                    "content": f"<tool_result>\nTool: {tc['name']}\nResult: {result}\n</tool_result>"
                })

    async def chat(self, model_id: str, messages: List[dict]) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model_id,
            "messages": messages,
            "stream": False
        }
        resp = await self.client.post(url, json=payload, timeout=None)
        if resp.status_code != 200:
            raise ValueError(f"Ollama error: {resp.text}")
        data = resp.json()
        return data["message"]["content"]

    async def shutdown(self):
        await self.client.aclose()
