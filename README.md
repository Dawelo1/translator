
# Translator API & GUI 🇵🇱→en

Projekt tłumaczący teksty z języka polskiego na angielski, wykorzystujący modele Opus-MT i mBART-50.

## Pliki
- `api.py` – backend (FastAPI), endpoint `/translate`
- `frontend.py` – GUI (Streamlit)
- `evaluate_translation.py` – skrypt do testowania i ewaluacji modeli tłumaczących **z polskiego na angielski**
- `requirements.txt` – zależności

## Uruchamianie lokalne
```bash
pip install -r requirements.txt
uvicorn api.api:app --reload
streamlit run frontend/frontend.py
````

## Testowanie modeli (ewaluacja)

Aby przetestować modele na losowo wybranych zdaniach **z języka polskiego na angielski** i wygenerować raport z wynikami BLEU:

```bash
python evaluate_translation.py lub python evaluate_translation.py --manual
```

Skrypt:

* Ładuje losowo 50 zdań z zestawu `opus_books` (PL→EN).
* Tłumaczy każde zdanie za pomocą modeli Opus-MT i mBART-50.
* Oblicza metrykę BLEU dla obu modeli.
* Zapisuje raport do `reports/evaluation_report.md`.
* Zapisuje szczegóły tłumaczeń w `reports/data.json`.
* Tworzy plik z testowymi danymi źródłowymi w `data/test_data.json`.

## Ważna uwaga dotycząca modeli

Model **Opus-MT** nie radzi sobie dobrze z tekstami zawierającymi wiele zdań naraz.
Dlatego tekst jest dzielony na pojedyncze zdania i tłumaczony osobno, co może powodować utratę kontekstu.

Model **mBART-50** radzi sobie lepiej z dłuższymi fragmentami, zachowując kontekst.

