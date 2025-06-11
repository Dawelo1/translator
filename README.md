
# Translator API & GUI 🇵🇱→en

Projekt tłumaczący teksty z języka polskiego na angielski, wykorzystujący modele Opus-MT i mBART-50.

## Pliki
- `api.py` – backend (FastAPI), endpoint `/translate`
- `frontend.py` – GUI (Streamlit)
- `evaluate_translation.py` – skrypt do testowania i ewaluacji modeli tłumaczących **z polskiego na angielski**
- `requirements.txt` – zależności

## Uruchamianie lokalne
```bash
docker-compose up --build
````



## Ważna uwaga dotycząca modeli

Model **Opus-MT** nie radzi sobie dobrze z tekstami zawierającymi wiele zdań naraz.
Dlatego tekst jest dzielony na pojedyncze zdania i tłumaczony osobno, co może powodować utratę kontekstu.

Model **mBART-50** radzi sobie lepiej z dłuższymi fragmentami, zachowując kontekst.



## Dokumentacja

https://Dawelo1.github.io/translator/
