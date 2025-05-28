import streamlit as st
import requests
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Translator GUI", page_icon="🌍", layout="wide")

st.title("🌍 Translator GUI")
st.markdown("Wprowadź tekst i wybierz model do tłumaczenia albo przetestuj oba modele na wielu przykładach.")

mode = st.radio("Tryb działania", ["Tłumaczenie", "Test"])

if mode == "Tłumaczenie":
    text = st.text_area("Tekst do przetłumaczenia", height=300)

    model_label = st.radio("Wybierz model tłumaczenia", ["Opus-MT", "mBART-50", "Oba modele"])
    model_map = {
        "Opus-MT": "opus",
        "mBART-50": "mbart"
    }

    if st.button("Przetłumacz"):
        if not text.strip():
            st.warning("Proszę wprowadzić tekst.")
        else:
            with st.spinner("Tłumaczenie..."):
                try:
                    if model_label == "Oba modele":
                        response_opus = requests.post(f"{API_URL}/translate", json={"text": text, "model": "opus"})
                        response_mbart = requests.post(f"{API_URL}/translate", json={"text": text, "model": "mbart"})

                        if response_opus.status_code == 200 and response_mbart.status_code == 200:
                            st.subheader("Opus-MT")
                            st.code(response_opus.json().get("translated_text", ""))
                            st.subheader("mBART-50")
                            st.code(response_mbart.json().get("translated_text", ""))
                        else:
                            st.error("Błąd tłumaczenia.")
                    else:
                        model_api = model_map[model_label]
                        response = requests.post(f"{API_URL}/translate", json={"text": text, "model": model_api})
                        if response.status_code == 200:
                            st.subheader(model_label)
                            st.code(response.json().get("translated_text", ""))
                        else:
                            st.error(f"Błąd API: {response.status_code}")
                except Exception as e:
                    st.error(f"Błąd połączenia: {e}")

elif mode == "Test":
    test_data_raw = st.text_area("Dane testowe (każdy wiersz: PL = EN)", height=300)

    if st.button("Przetestuj modele"):
        if not test_data_raw.strip():
            st.warning("Wprowadź dane testowe.")
        else:
            try:
                # Parsowanie danych do formatu JSON
                examples = []
                for line in test_data_raw.strip().splitlines():
                    if "=" not in line:
                        continue
                    parts = line.split("=", maxsplit=1)
                    pl = parts[0].strip()
                    en = parts[1].strip()
                    if pl and en:
                        examples.append({"pl": pl, "en": en})

                if not examples:
                    st.warning("Nie znaleziono poprawnych danych wejściowych.")
                else:
                    with st.spinner("Ładowanie danych i ewaluacja modeli..."):
                        r1 = requests.post(f"{API_URL}/load-test-data", json=examples)
                        if r1.status_code != 200:
                            st.error("Błąd ładowania danych testowych.")
                        else:
                            r2 = requests.get(f"{API_URL}/evaluate")
                            if r2.status_code == 200:
                                result = r2.json()
                                bleu = result.get("bleu_scores", {})
                                trans = result.get("translations", [])

                                st.success("Ewaluacja zakończona.")
                                st.metric("BLEU Opus-MT", bleu.get("opus", 0))
                                st.metric("BLEU mBART-50", bleu.get("mbart", 0))

                                st.divider()
                                for i, item in enumerate(trans, 1):
                                    st.markdown(f"### Przykład {i}")
                                    st.markdown(f"- **PL:** {item['source_pl']}")
                                    st.markdown(f"- **EN (referencja):** {item['reference_en']}")
                                    st.markdown(f"- **Opus-MT:** `{item['opus_mt']}`")
                                    st.markdown(f"- **mBART-50:** `{item['mbart']}`")
                                    st.divider()
                            else:
                                st.error("Błąd podczas ewaluacji.")
            except Exception as e:
                st.error(f"Błąd testowania: {e}")
