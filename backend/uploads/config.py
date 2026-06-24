from dotenv import dotenv_values


_config = dotenv_values(".env")


class Config:
    OLLAMA_URL = _config.get("OLLAMA_URL")
    OLLAMA_MODEL = _config.get("OLLAMA_MODEL")
    API_TOKEN = _config.get("API_TOKEN")
    CHROMA_PATH = _config.get("CHROMA_PATH")
    LOG_PATH = _config.get("LOG_PATH")


config = Config()