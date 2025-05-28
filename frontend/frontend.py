import streamlit as st
import requests
import time
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Translator GUI", page_icon="🌍", layout="wide")

st.title("🌍 Translator GUI")
st.markdown("Wprowadź tekst i wybierz model do tłumaczenia albo przetestuj oba modele na wielu przykładach.")

mode = st.radio("Tryb działania", ["Tłumaczenie", "Test"])

model_map = {
    "Opus-MT": "opus",
    "mBART-50": "mbart"
}

def display_result(title, text, elapsed_time):
    st.subheader(title)
    st.code(text, language=None)
    if elapsed_time is not None:
        st.caption(f"Czas tłumaczenia: {elapsed_time:.2f} sekundy")

if mode == "Tłumaczenie":
    text = st.text_area("Tekst do przetłumaczenia", height=300)

    model_label = st.radio("Wybierz model tłumaczenia", ["Opus-MT", "mBART-50", "Oba modele"])

    if st.button("Przetłumacz"):
        if not text.strip():
            st.warning("Proszę wprowadzić tekst.")
        else:
            with st.spinner("Tłumaczenie..."):
                try:
                    if model_label == "Oba modele":
                        start_opus = time.perf_counter()
                        response_opus = requests.post(f"{API_URL}/translate", json={"text": text, "model": "opus"})
                        end_opus = time.perf_counter()
                        time_opus = end_opus - start_opus

                        start_mbart = time.perf_counter()
                        response_mbart = requests.post(f"{API_URL}/translate", json={"text": text, "model": "mbart"})
                        end_mbart = time.perf_counter()
                        time_mbart = end_mbart - start_mbart

                        if response_opus.status_code == 200 and response_mbart.status_code == 200:
                            translated_opus = response_opus.json().get("translated_text", "")
                            translated_mbart = response_mbart.json().get("translated_text", "")
                            col1, col2 = st.columns(2)
                            with col1:
                                display_result("Opus-MT", translated_opus, time_opus)
                            with col2:
                                display_result("mBART-50", translated_mbart, time_mbart)
                        else:
                            st.error("Błąd podczas tłumaczenia jednym lub dwoma modelami.")
                    else:
                        api_model = model_map.get(model_label)
                        start = time.perf_counter()
                        response = requests.post(f"{API_URL}/translate", json={"text": text, "model": api_model})
                        end = time.perf_counter()
                        elapsed = end - start

                        if response.status_code == 200:
                            translated_text = response.json().get("translated_text", "")
                            display_result(model_label, translated_text, elapsed)
                        else:
                            st.error(f"Błąd API: {response.status_code}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Błąd połączenia: {e}")

elif mode == "Test":
    st.markdown("**Format danych testowych:** każdy wiersz w formacie `PL = EN` (np. `To jest test = This is a test`).")
    test_data_raw = st.text_area("Dane testowe", height=300, placeholder="Przykład:\nTo jest test = This is a test")

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
