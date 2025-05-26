import streamlit as st
import requests

st.set_page_config(page_title="Translator GUI", page_icon="🌍")

st.title("🌍 Translator GUI")
st.markdown("Wprowadź tekst, wybierz model i kierunek tłumaczenia.")

# Wprowadzenie tekstu
text = st.text_area("Tekst do przetłumaczenia", height=150)

# Wybór modelu
model_label = st.radio("Model tłumaczenia", ["Opus-MT", "mBART-50"])

# Wybór kierunku
direction = st.radio("Kierunek tłumaczenia", ["Polski ➜ Angielski", "Angielski ➜ Polski"])

# Mapa modelu GUI → API
model_map = {
    "Opus-MT": "opus",
    "mBART-50": "mbart"
}

# Mapa kierunku GUI → języki
lang_map = {
    "Polski ➜ Angielski": ("pl", "en"),
    "Angielski ➜ Polski": ("en", "pl")
}

translated = None

if st.button("Przetłumacz"):
    if not text.strip():
        st.warning("Proszę wprowadzić tekst.")
    else:
        with st.spinner("Tłumaczenie..."):
            try:
                api_model = model_map[model_label]
                src_lang, tgt_lang = lang_map[direction]

                payload = {
                    "text": text,
                    "model": api_model,
                    "source_lang": src_lang,
                    "target_lang": tgt_lang
                }

                print(f"[DEBUG] Wysyłam zapytanie: {payload}")
                response = requests.post("http://localhost:8000/translate", json=payload)

                print(f"[DEBUG] Status code: {response.status_code}")
                print(f"[DEBUG] Response JSON: {response.text}")

                if response.status_code == 200:
                    translated = response.json().get("translated_text", "")
                else:
                    st.error(f"Błąd API: {response.status_code}")
                    st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Błąd połączenia: {e}")
                print(f"[DEBUG] Request error: {e}")

# Wyświetlenie tłumaczenia
if translated:
    st.success("Przetłumaczony tekst:")
    st.code(translated, language="text")
