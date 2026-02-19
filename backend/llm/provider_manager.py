from .ollama_provider import OllamaProvider

class LLMManager:
    def __init__(self, provider: str = "ollama", model: str | None = None):
        self.provider_name = provider.lower()
        self.model = model
        if self.provider_name == "ollama":
            self.provider = OllamaProvider(model_name=model or "phi3")
        else:
            raise ValueError(f"Inavalid provider: {provider}")
    
    def generate(self, messages: list):
        return self.provider.generate(messages)