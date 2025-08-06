import os

from langchain_ollama import OllamaLLM

from utils.constants import OLLAMA_TEST_SERVER_URL
from dotenv import load_dotenv

load_dotenv()


class BaseOllamaLLM:

    def __init__(self, model, base_url=None, num_ctx=10000,
                 temperature=0.0, mirostat=2, mirostat_eta=0.5, mirostat_tau=4, **kwargs):
        self.model = model
        self.base_url = os.getenv(OLLAMA_TEST_SERVER_URL)
        self.num_ctx = num_ctx
        self.temperature = temperature
        self.mirostat = mirostat
        self.mirostat_eta = mirostat_eta
        self.mirostat_tau = mirostat_tau
        self.extra_kwargs = kwargs

    def create(self):
        return OllamaLLM(
            model=self.model,
            base_url=self.base_url,
            num_ctx=self.num_ctx,
            temperature=self.temperature,
            mirostat=self.mirostat,
            mirostat_eta=self.mirostat_eta,
            mirostat_tau=self.mirostat_tau,
            **self.extra_kwargs
        )


class SingletonLLM(type):
    """Metaclass to implement the Singleton-Pattern"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Llama3(BaseOllamaLLM, metaclass=SingletonLLM):
    def __init__(self, **kwargs):
        super().__init__(model="llama3.3:latest", **kwargs)


class QwenVision(BaseOllamaLLM, metaclass=SingletonLLM):
    def __init__(self, **kwargs):
        super().__init__(model="qwen2.5vl:72b", **kwargs)


class Phi4(BaseOllamaLLM, metaclass=SingletonLLM):
    def __init__(self, **kwargs):
        super().__init__(model="phi4:latest", **kwargs)


class Phi4_friendly(BaseOllamaLLM, metaclass=SingletonLLM):
    def __init__(self, **kwargs):
        super().__init__(model="phi4:latest", temperature=0.3, **kwargs)
