import streamlit as st
import requests

st.set_page_config(page_title="Translator GUI", page_icon="🌍")

st.title("🌍 Translator GUI")
st.markdown("Wprowadź tekst i wybierz model do tłumaczenia.")

# Formularz użytkownika
text = st.text_area("Tekst do przetłumaczenia", height=150)

# Użycie radio do wyboru modelu
model_label = st.radio("Wybierz model tłumaczenia", ["Opus-MT", "mBART-50"])

# Mapa nazw GUI -> API
model_map = {
    "Opus-MT": "opus",
    "mBART-50": "mbart"
}

translated = None

if st.button("Przetłumacz"):
    if not text.strip():
        st.warning("Proszę wprowadzić tekst.")
    else:
        with st.spinner("Tłumaczenie..."):
            try:
                api_model = model_map.get(model_label)
                payload = {"text": text, "model": api_model}
                
                response = requests.post("http://localhost:8000/translate", json=payload)

                if response.status_code == 200:
                    translated = response.json().get("translated_text", "")
                else:
                    st.error(f"Błąd API: {response.status_code}")
                    st.json(response.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Błąd połączenia: {e}")
                print(f"[DEBUG] Request error: {e}")

# Wyświetlanie przetłumaczonego tekstu
if translated:
    st.success("Przetłumaczony tekst:")
    st.code(translated, language="text")
