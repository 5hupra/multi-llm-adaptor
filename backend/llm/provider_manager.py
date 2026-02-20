from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider
import os

class LLMProviderManager:
    def __init__(self, provider: str = "auto", model: str | None = None, api_key: str | None=None):
        self.provider_name = (provider or "auto").lower()
        self.model = model
        self.api_key = api_key

    def load_provider(self):
        if self.provider_name == "openai":
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("API key required for OpenAI provider")
            return OpenAIProvider(
                api_key=api_key,
                model_name=self.model or "gpt-4o-mini"
            )
        if self.provider_name == "ollama":
            return OllamaProvider(model_name=self.model or "phi3")
        if self.provider_name == "auto":
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            
            if api_key:
                return OpenAIProvider(api_key=self.api_key, model_name=self.model or "gpt-4o-mini")
            return OllamaProvider(model_name=self.model or"phi3")
        
        raise ValueError(f"Invalid provider: {self.provider_name}")
    
    def generate(self, messages: list, stream: bool = False):
        try:
            provider = self.load_provider()
            return provider.generate(messages, stream=stream)
        
        except Exception:
            fallback = OllamaProvider(model_name=self.model or "phi3")
            return fallback.generate(messages, stream=stream)