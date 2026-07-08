import os
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from duckduckgo_search import DDGS

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    # Fallback if mcp is not fully installed
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MCPManager")

class MCPManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MCPManager, cls).__new__(cls)
            cls._instance.servers = {} # name -> { 'session': session, 'process': process }
            cls._instance.native_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Searches the web using DuckDuckGo to find current information, news, or answers.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query."
                                }
                            },
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "execute_python",
                        "description": "Executes a python script locally to manipulate files or run tasks.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "The python code to execute."
                                }
                            },
                            "required": ["code"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "execute_shell_command",
                        "description": "Executes a shell command (PowerShell/Cmd on Windows, Bash on Linux) on the host machine. Use with caution.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The command line string to execute."
                                }
                            },
                            "required": ["command"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "read_file",
                        "description": "Reads the contents of a local file.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The absolute or relative path to the file."
                                }
                            },
                            "required": ["file_path"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "write_file",
                        "description": "Writes content to a local file, overwriting it if it exists.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The absolute or relative path to the file."
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content to write to the file."
                                }
                            },
                            "required": ["file_path", "content"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "deep_research",
                        "description": "Autonomously searches the web and compiles a detailed markdown report on a topic.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "topic": {
                                    "type": "string",
                                    "description": "The topic to research deeply."
                                }
                            },
                            "required": ["topic"]
                        }
                    }
                }
            ]
            cls._instance.mcp_tools = [] # Fetched from connected MCP servers
            cls._instance.tool_routing_map = {} # tool_name -> server_name (None for native)
        return cls._instance

    async def initialize(self):
        # Register native tools in the map
        for t in self.native_tools:
            self.tool_routing_map[t["function"]["name"]] = None
            
        # Try loading MCP servers from a local mcp.json config if it exists
        config_path = os.path.join(os.getcwd(), "mcp.json")
        if os.path.exists(config_path) and StdioServerParameters:
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    
                for server_name, server_config in config.get("mcpServers", {}).items():
                    await self._connect_server(server_name, server_config)
            except Exception as e:
                logger.error(f"Failed to load MCP servers: {e}")
                
        # Register them all
        await self._refresh_tools()

    async def _connect_server(self, name: str, config: dict):
        command = config.get("command")
        args = config.get("args", [])
        env = config.get("env", {})
        
        # Merge env
        merged_env = os.environ.copy()
        merged_env.update(env)
        
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=merged_env
        )
        
        # NOTE: In a production setting we'd use AsyncExitStack, but for a singleton
        # we will manually manage the context managers.
        # This is a simplified connection for Aether.
        # Anthropic's mcp client uses async context managers heavily.
        pass # Full MCP connection requires careful async context management. 
             # We will implement a mock connection for the user's Roblox server if they didn't configure it,
             # or simply rely on the native tools for now until mcp.json is populated.

    async def _refresh_tools(self):
        self.mcp_tools = []
        # Native tools are already in self.native_tools
        # If we had connected servers, we would do: session.list_tools()

    def get_all_tools(self) -> List[Dict[str, Any]]:
        return self.native_tools + self.mcp_tools

    async def execute_tool(self, tool_name: str, args: dict) -> str:
        server_name = self.tool_routing_map.get(tool_name)
        
        if server_name is None:
            # Execute native tool
            if tool_name == "web_search":
                return await self._execute_web_search(args.get("query", ""))
            elif tool_name == "execute_python":
                return await self._execute_python(args.get("code", ""))
            elif tool_name == "execute_shell_command":
                return await self._execute_shell_command(args.get("command", ""))
            elif tool_name == "read_file":
                return await self._execute_read_file(args.get("file_path", ""))
            elif tool_name == "write_file":
                return await self._execute_write_file(args.get("file_path", ""), args.get("content", ""))
            elif tool_name == "deep_research":
                return await self._execute_deep_research(args.get("topic", ""))
            else:
                return f"Error: Tool {tool_name} not found."
        else:
            # Execute MCP tool
            session = self.servers.get(server_name, {}).get("session")
            if not session:
                return f"Error: Server {server_name} not connected."
            
            try:
                result = await session.call_tool(tool_name, arguments=args)
                if result.isError:
                    return f"Error from tool: {result.content}"
                
                # Extract text content
                texts = [c.text for c in result.content if c.type == "text"]
                return "\n".join(texts)
            except Exception as e:
                return f"Failed to execute MCP tool: {e}"

    async def _execute_web_search(self, query: str) -> str:
        try:
            results = DDGS().text(query, max_results=5)
            if not results:
                return "No results found."
            
            formatted = []
            for r in results:
                formatted.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")
            return "\n".join(formatted)
        except Exception as e:
            return f"Search failed: {e}"
            
    async def _execute_python(self, code: str) -> str:
        # In a real desktop app, we might want to sandbox this, but Aether is a god-mode local engine.
        try:
            import contextlib
            import io
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exec(code, globals())
            return stdout.getvalue() or "Code executed successfully with no output."
        except Exception as e:
            return f"Python Error: {e}"

    async def _execute_shell_command(self, command: str) -> str:
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            output = ""
            if stdout:
                output += f"STDOUT:\n{stdout.decode('utf-8', errors='replace')}\n"
            if stderr:
                output += f"STDERR:\n{stderr.decode('utf-8', errors='replace')}\n"
                
            if not output:
                output = f"Command executed successfully with return code {process.returncode} and no output."
                
            return output
        except Exception as e:
            return f"Shell Execution Error: {e}"

    async def _execute_read_file(self, file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Read File Error: {e}"

    async def _execute_write_file(self, path: str, content: str) -> str:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    async def _execute_deep_research(self, topic: str) -> str:
        try:
            from duckduckgo_search import DDGS
            import urllib.request
            from bs4 import BeautifulSoup
            
            # Step 1: Initial broad search
            results = DDGS().text(topic, max_results=3)
            compiled_report = f"# Deep Research Report: {topic}\n\n"
            
            for res in results:
                url = res.get("href")
                compiled_report += f"## Source: [{res.get('title')}]({url})\n"
                compiled_report += f"**Summary:** {res.get('body')}\n\n"
                
                # Optional: Try to scrape the actual page content for deeper insight
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req, timeout=5).read()
                    soup = BeautifulSoup(html, 'html.parser')
                    paragraphs = soup.find_all('p')
                    text = " ".join([p.text for p in paragraphs][:5]) # Get first 5 paragraphs
                    if text:
                        compiled_report += f"**Excerpt:** {text}\n\n"
                except Exception:
                    pass
                    
            return compiled_report
        except Exception as e:
            return f"Deep research failed: {str(e)}"
