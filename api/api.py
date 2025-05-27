import sys
import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from utils.translation_utils import init_models, translate_opus, translate_mbart

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    model: str  # "opus" lub "mbart"

opus_model, mbart_tokenizer, mbart_model = init_models()

@app.post(
    "/translate",
    summary="Tłumaczenie tekstu PL->EN",
    description="Przetłumacz tekst z języka polskiego na angielski. Wybierz model: 'opus' (MarianMT) lub 'mbart' (mBART)."
)
def translate(request: TranslateRequest):
    text = request.text
    model = request.model.lower()

    if model == "opus":
        result = translate_opus(text, opus_model)
    elif model == "mbart":
        result = translate_mbart(text, mbart_tokenizer, mbart_model)
    else:
        return {"error": "Invalid model. Choose 'opus' or 'mbart'."}

    return {"translated_text": result}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
