import aiohttp
from typing import List, Dict, Any

class AetherSwarm:
    """
    P2P Network Node for Distributed Reasoning Swarms.
    Connects to other Aether instances to distribute cognitive load.
    """
    def __init__(self):
        self.peers = set()

    def connect(self, peer_url: str):
        """Register a new peer in the swarm."""
        # Ensure url doesn't end with slash
        clean_url = peer_url.rstrip("/")
        self.peers.add(clean_url)
        return list(self.peers)

    def disconnect(self, peer_url: str):
        """Remove a peer from the swarm."""
        clean_url = peer_url.rstrip("/")
        if clean_url in self.peers:
            self.peers.remove(clean_url)

    async def broadcast(self, query: str) -> List[Dict[str, Any]]:
        """
        Broadcast a reasoning task to all connected peers and collect their cognitive traces.
        """
        results = []
        async with aiohttp.ClientSession() as session:
            for peer in list(self.peers):
                try:
                    # We hit the peer's standard API, so they use their own Cortex graph
                    async with session.post(
                        f"{peer}/api/chat/completions", 
                        json={"messages": [{"role": "user", "content": query}], "stream": False},
                        timeout=aiohttp.ClientTimeout(total=30)
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            results.append({"peer": peer, "result": data})
                        else:
                            results.append({"peer": peer, "error": f"HTTP {resp.status}"})
                except Exception as e:
                    results.append({"peer": peer, "error": str(e)})
                    
        return results
