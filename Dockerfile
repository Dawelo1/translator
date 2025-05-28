FROM python:3.10-slim

WORKDIR /app

# Skopiuj wszystkie potrzebne katalogi
COPY ./api /app/api
COPY ./utils /app/utils
COPY ./evaluation /app/evaluation

# Ustaw PYTHONPATH, żeby można było importować utils.*
ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app/api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
