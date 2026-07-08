import os
import json
import time
import asyncio
from typing import List, AsyncGenerator, Tuple
from anthropic import AsyncAnthropic
from aether.providers.base import BaseProvider, ModelInfo
from aether.mcp_client import MCPManager

class ClaudeProvider(BaseProvider):
    def __init__(self):
        super().__init__("claude", "Anthropic Claude", "cloud")
        self.client = None
        self._api_key = ""
        
    async def initialize(self):
        self._api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if self._api_key:
            self.client = AsyncAnthropic(api_key=self._api_key)
        
        self.models = [
            ModelInfo(
                "claude-sonnet-4-20250514", 
                "Claude Sonnet 4", 
                200000, 
                "Latest and most intelligent Sonnet model",
                ["vision", "tools", "fast", "reasoning"]
            ),
            ModelInfo(
                "claude-3-5-sonnet-20241022", 
                "Claude 3.5 Sonnet v2", 
                200000, 
                "Previous generation Sonnet, still excellent",
                ["vision", "tools", "fast"]
            ),
            ModelInfo(
                "claude-3-5-haiku-20241022", 
                "Claude 3.5 Haiku", 
                200000, 
                "Fastest and most compact model",
                ["vision", "fast"]
            ),
            ModelInfo(
                "claude-3-opus-20240229", 
                "Claude 3 Opus", 
                200000, 
                "Highest performance on complex tasks",
                ["vision", "tools", "reasoning"]
            ),
        ]
        self.status = "connected" if self._api_key else "disconnected"

    def set_api_key(self, key: str):
        self._api_key = key
        os.environ["ANTHROPIC_API_KEY"] = key
        if key:
            self.client = AsyncAnthropic(api_key=key)
            self.status = "connected"
        else:
            self.client = None
            self.status = "disconnected"
        
    async def test_connection(self) -> Tuple[bool, float, str]:
        if not self.client or not self._api_key:
            return False, 0.0, "API key not configured"
            
        start = time.time()
        try:
            await self.client.messages.create(
                max_tokens=10,
                messages=[{"role": "user", "content": "hello"}],
                model="claude-3-5-haiku-20241022"
            )
            latency = (time.time() - start) * 1000
            self.status = "connected"
            return True, latency, ""
        except Exception as e:
            self.status = "error"
            return False, 0.0, str(e)
            
    def _convert_tools_to_anthropic(self, tools: List[dict]) -> List[dict]:
        anthropic_tools = []
        for t in tools:
            func = t.get("function", {})
            anthropic_tools.append({
                "name": func.get("name"),
                "description": func.get("description", ""),
                "input_schema": func.get("parameters", {"type": "object", "properties": {}})
            })
        return anthropic_tools

    async def stream_chat(self, model_id: str, messages: List[dict]) -> AsyncGenerator[str, None]:
        if not self.client:
            raise ValueError("Anthropic API key not configured.")
            
        mcp = MCPManager()
        raw_tools = mcp.get_all_tools()
        tools = self._convert_tools_to_anthropic(raw_tools)
        
        # We need to maintain the internal message history for the recursive loop
        current_messages = []
        for msg in messages:
            # Anthropic expects 'user' or 'assistant'
            # We map 'system' to system param, but for simplicity here we assume standard format.
            if msg["role"] == "system":
                # System is handled separately in Anthropic, skipping for now
                continue
            current_messages.append({"role": msg["role"], "content": msg["content"]})
            
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        
        max_loops = 5
        for _ in range(max_loops):
            kwargs = {
                "max_tokens": 4096,
                "messages": current_messages,
                "model": model_id,
            }
            if system_msg:
                kwargs["system"] = system_msg
            if tools:
                kwargs["tools"] = tools

            tool_calls = []
            
            async with self.client.messages.stream(**kwargs) as stream:
                async for event in stream:
                    if event.type == "text":
                        yield event.text
                    elif event.type == "content_block_start" and event.content_block.type == "tool_use":
                        tool_calls.append({
                            "id": event.content_block.id,
                            "name": event.content_block.name,
                            "input": ""
                        })
                        # Yield a metadata chunk so the UI knows we are using a tool!
                        meta = {"type": "metadata", "metadata": {"tool_call": event.content_block.name}}
                        yield f"\n\n```metadata\n{json.dumps(meta)}\n```\n\n"
                    elif event.type == "content_block_delta" and event.delta.type == "input_json_delta":
                        if tool_calls:
                            tool_calls[-1]["input"] += event.delta.partial_json
                            
            if not tool_calls:
                break # We're done! No more tools to call.
                
            # Execute tool calls
            assistant_message_content = []
            for tc in tool_calls:
                # Add the tool_use to the assistant's message content so Anthropic knows what happened
                args = json.loads(tc["input"]) if tc["input"] else {}
                assistant_message_content.append({
                    "type": "tool_use",
                    "id": tc["id"],
                    "name": tc["name"],
                    "input": args
                })
                
                # Actually execute it
                result = await mcp.execute_tool(tc["name"], args)
                
                current_messages.append({
                    "role": "assistant", 
                    "content": assistant_message_content
                })
                current_messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tc["id"],
                            "content": result
                        }
                    ]
                })

    async def chat(self, model_id: str, messages: List[dict]) -> str:
        # Simplified non-streaming version for now
        if not self.client:
            raise ValueError("Anthropic API key not configured.")
        response = await self.client.messages.create(
            max_tokens=4096,
            messages=messages,
            model=model_id
        )
        return response.content[0].text

    async def shutdown(self):
        pass
