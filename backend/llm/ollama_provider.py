import httpx
from .base_provider import BaseLLMProvider

class  OllamaProvider(BaseLLMProvider):
    def __init__(self, model_name: str="phi3"):
        self.model_name=model_name
        self.url = "http://localhost:11434/api/generate"

    def generate(self,
                 messages: list,
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 stream: bool = False
    ) -> dict:
        
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"{role}: {content}")
        prompt = "\n".join(prompt_parts)

        payload = {
            "model" : self.model_name,
            "prompt": prompt,
            "stream": stream
        }

        if not stream:
            response = httpx.post(self.url, json=payload, timeout=180)
            response.raise_for_status()

            data = response.json()
            return {
                "text": data.get("response", "").strip(),
                "usage": {},
                "model": self.model_name,
                "provider": "ollama",
            }
        #streaming
        else:
            with httpx.stream("POST", self.url, json=payload, timeout=180) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        import json
                        chunk = json.loads(line.decode("utf-8"))

                        if "response" in chunk:
                           yield chunk["response"]
                    except Exception:
                        continue
