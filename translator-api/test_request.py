import requests

url = "http://localhost:8000/translate"
payload = {
    "text": "Mam na imię Jan i lubię programować.",
    "model": "t5"
}

response = requests.post(url, json=payload)
print(response.json())
