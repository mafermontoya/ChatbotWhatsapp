import requests

url = "https://nonruinable-uncheckmated-dalila.ngrok-free.dev/webhook"
data = {"event": "test", "ping": True}

try:
    response = requests.post(url, json=data)
    print("Código de respuesta:", response.status_code)
    print("Respuesta:", response.text)
except Exception as e:
    print("Error al conectar:", e)
