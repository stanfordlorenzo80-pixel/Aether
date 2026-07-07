import math
import json
import os
from collections import Counter
from typing import List, Dict, Any

class LocalVectorStore:
    """
    A lightweight, pure-Python vector database.
    Uses TF-style frequency vectors and cosine similarity for blazing fast local context retrieval.
    Persists to disk automatically.
    """
    def __init__(self, db_path="aether_memory.json"):
        self.db_path = db_path
        self.memories = []
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.memories = json.load(f)

    def _save(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2)

    def _get_vector(self, text: str) -> Dict[str, int]:
        words = text.lower().replace('.', '').replace(',', '').split()
        return dict(Counter(words))

    def _cosine_similarity(self, vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def store_episode(self, content: str, metadata: Dict[str, Any] = None):
        """Stores a new memory and its computed vector."""
        if not metadata: metadata = {}
        memory = {
            "content": content,
            "vector": self._get_vector(content),
            "metadata": metadata
        }
        self.memories.append(memory)
        self._save()

    def retrieve_relevant(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Retrieves the top k most relevant memories based on cosine similarity."""
        if not self.memories: return []
        
        query_vec = self._get_vector(query)
        scored_memories = []
        
        for mem in self.memories:
            score = self._cosine_similarity(query_vec, mem["vector"])
            scored_memories.append({"score": score, "content": mem["content"], "metadata": mem["metadata"]})
            
        # Sort by score descending
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        
        # Filter out zero scores and return top k
        return [m for m in scored_memories if m["score"] > 0][:k]
