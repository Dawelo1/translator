# Użyj lekkiego obrazu Pythona
FROM python:3.10-slim

# Ustaw katalog roboczy
WORKDIR /frontend

# Skopiuj pliki aplikacji i requirements
COPY . /frontend
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Wyłącz telemetry Streamlit
ENV STREAMLIT_TELEMETRY_DISABLED=true

# Ustaw zmienną środowiskową na domyślny adres API, jeśli nie podano
ENV API_URL=http://localhost:8000

# Otwórz port Streamlit
EXPOSE 8501

# Uruchom aplikację Streamlit
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
