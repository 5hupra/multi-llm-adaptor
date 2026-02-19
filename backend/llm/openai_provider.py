import httpx
from .base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model_name:str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model_name = model_name
        self.url = "https://api.openai.com/v1/chat/completions"

    def generate(self,
                 messages: list,
                 temperature: float = 0.7,
                 max_tokens: int = 500,
                 stream: bool = False
    ) -> dict:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = httpx.post(self.url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data=response.json()

        text = data["choices"][0]["message"]["content"]

        return {
            "text": text.strip(),
            "usage": data.get("usage", {}),
            "model": self.model_name,
            "provider": "openai"
        }