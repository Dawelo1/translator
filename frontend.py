import streamlit as st
import requests

st.set_page_config(page_title="Translator GUI", page_icon="🌍")

st.title("🌍 Translator GUI")
st.markdown("Wprowadź tekst i wybierz model do tłumaczenia.")

# Formularz użytkownika
text = st.text_area("Tekst do przetłumaczenia", height=150)

# Użycie radio do wyboru modelu, dodajemy opcję "Oba modele"
model_label = st.radio("Wybierz model tłumaczenia", ["Opus-MT", "mBART-50", "Oba modele"])

# Mapa nazw GUI -> API
model_map = {
    "Opus-MT": "opus",
    "mBART-50": "mbart"
}

translated_opus = None
translated_mbart = None
error_msg = None

if st.button("Przetłumacz"):
    if not text.strip():
        st.warning("Proszę wprowadzić tekst.")
    else:
        with st.spinner("Tłumaczenie..."):
            try:
                if model_label == "Oba modele":
                    # Wywołujemy API dwa razy, raz dla każdego modelu
                    payload_opus = {"text": text, "model": "opus"}
                    payload_mbart = {"text": text, "model": "mbart"}

                    response_opus = requests.post("http://localhost:8000/translate", json=payload_opus)
                    response_mbart = requests.post("http://localhost:8000/translate", json=payload_mbart)

                    if response_opus.status_code == 200 and response_mbart.status_code == 200:
                        translated_opus = response_opus.json().get("translated_text", "")
                        translated_mbart = response_mbart.json().get("translated_text", "")
                    else:
                        error_msg = "Błąd podczas tłumaczenia jednym lub dwoma modelami."
                else:
                    api_model = model_map.get(model_label)
                    payload = {"text": text, "model": api_model}
                    response = requests.post("http://localhost:8000/translate", json=payload)

                    if response.status_code == 200:
                        if api_model == "opus":
                            translated_opus = response.json().get("translated_text", "")
                        else:
                            translated_mbart = response.json().get("translated_text", "")
                    else:
                        error_msg = f"Błąd API: {response.status_code}"

            except requests.exceptions.RequestException as e:
                error_msg = f"Błąd połączenia: {e}"
                print(f"[DEBUG] Request error: {e}")

if error_msg:
    st.error(error_msg)

# Wyświetlanie wyników
if model_label == "Oba modele" and translated_opus and translated_mbart:
    col1, col2 = st.columns(2)
    with col1:
        st.success("Opus-MT:")
        st.code(translated_opus, language="text")
    with col2:
        st.success("mBART-50:")
        st.code(translated_mbart, language="text")
else:
    if translated_opus:
        st.success("Przetłumaczony tekst (Opus-MT):")
        st.code(translated_opus, language="text")
    if translated_mbart:
        st.success("Przetłumaczony tekst (mBART-50):")
        st.code(translated_mbart, language="text")
