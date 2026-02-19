from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider

class LLMProviderManager:
    def __init__(self, provider: str = "auto", model: str | None = None):
        self.provider_name = (provider or "auto").lower()
        self.model = model
        

    def load_provider(self):
        if self.provider_name == "openai":
            if not self.model:
                raise ValueError("API key required for OpenAI provider")
            return OpenAIProvider(
                api_key=self.model
            )
        if self.provider_name == "ollama":
            return OllamaProvider(model_name=self.model or "phi3")
        if self.provider_name == "auto":
            return OllamaProvider(model_name=self.model or"phi3")
        
        raise ValueError(f"Invalid provider: {self.provider_name}")
    
    def generate(self, messages: list):
        try:
            provider = self.load_provider()
            return provider.generate(messages)
        
        except Exception:
            fallback = OllamaProvider(model_name=self.model or "phi3")
            return fallback.generate(messages)