import requests
import json
from core.config import OLLAMA_URL, OLLAMA_MODEL


def stream_llm(prompt):

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():

        if line:

            data = json.loads(line)

            token = data.get("response", "")

            if token:
                yield token