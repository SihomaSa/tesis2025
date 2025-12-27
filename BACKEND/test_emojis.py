import requests
import json

url = "http://localhost:8000/api/analysis/batch"

# Textos con emojis y acentos
payload = {
    "texts": [
        "La UNMSM es bacán! ❤️",
        "Qué roche la administración 😒", 
        "Más o menos la infraestructura 🤔"
    ],
    "include_details": True
}

print("Enviando request con emojis...")
response = requests.post(url, json=payload)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")