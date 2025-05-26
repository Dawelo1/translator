# Translator API & GUI 🇵🇱→🇬🇧

Projekt tłumaczący teksty z języka polskiego na angielski, wykorzystujący modele Opus-MT i mBART-50.

## Pliki
- `api.py` – backend (FastAPI), endpoint `/translate`
- `frontend.py` – GUI (Streamlit)
- `requirements.txt` – zależności

## Uruchamianie lokalne
```bash
pip install -r requirements.txt
uvicorn api:app --reload
streamlit run frontend.py

opus-Mt nie radzi sobie z wieloma zdaniami dlatego zaimplementowane jest w kodzie dzielenie tekstu na pojedyncze zdania i tłumaczenia ich pojedynczo. moze przez to gubic kontekst.
