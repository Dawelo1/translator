import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from datasets import Dataset
from utils.translation_utils import init_models, translate_opus, translate_mbart, evaluate_models_on_dataset

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    model: str  # "opus" lub "mbart"

class TranslationExample(BaseModel):
    pl: str
    en: str

# Globalna zmienna do przechowywania danych testowych
loaded_test_data = []

# Inicjalizacja modeli przy starcie
opus_model, mbart_tokenizer, mbart_model = init_models()

@app.post("/translate", summary="Tłumaczenie tekstu PL->EN")
def translate(request: TranslateRequest):
    text = request.text
    model = request.model.lower()

    if model == "opus":
        result = translate_opus(text, opus_model)
    elif model == "mbart":
        result = translate_mbart(text, mbart_tokenizer, mbart_model)
    else:
        raise HTTPException(status_code=400, detail="Invalid model. Choose 'opus' or 'mbart'.")

    return {"translated_text": result}

@app.post("/load-test-data", summary="Załaduj dane testowe do pamięci")
def load_test_data(data: List[TranslationExample]):
    global loaded_test_data
    loaded_test_data = [{"translation": {"pl": item.pl, "en": item.en}} for item in data]
    return {"message": f"Załadowano {len(loaded_test_data)} przykładów testowych."}

@app.get("/evaluate", summary="Ewaluacja modeli na załadowanych danych")
def evaluate():
    if not loaded_test_data:
        raise HTTPException(status_code=400, detail="Brak załadowanych danych testowych. Użyj /load-test-data najpierw.")

    dataset = Dataset.from_list(loaded_test_data)

    opus_bleu, mbart_bleu, opus_preds, mbart_preds = evaluate_models_on_dataset(
        dataset, opus_model, mbart_tokenizer, mbart_model, return_predictions=True
    )

    results = []
    for example, opus_pred, mbart_pred in zip(dataset, opus_preds, mbart_preds):
        results.append({
            "source_pl": example["translation"]["pl"],
            "reference_en": example["translation"]["en"],
            "opus_mt": opus_pred,
            "mbart": mbart_pred
        })

    return {
        "bleu_scores": {
            "opus": round(opus_bleu, 2),
            "mbart": round(mbart_bleu, 2)
        },
        "translations": results
    }

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
