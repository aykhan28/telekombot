import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def ollama_chat(prompt):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120, stream=True)
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        full_response += data["response"]
                    elif "message" in data:
                        full_response += data["message"]
                except Exception:
                    continue
        return full_response.strip() if full_response else "Ollama'dan yanıt alınamadı."
    except requests.exceptions.RequestException as e:
        return f"Ollama bağlantı hatası: {e}"
    except Exception as e:
        return f"Ollama yanıtı işlenemedi: {e}"