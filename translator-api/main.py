from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, MBartForConditionalGeneration, MBart50TokenizerFast

app = FastAPI()

# Definicja modelu requestu
class TranslateRequest(BaseModel):
    text: str
    model: str  # "opus" lub "mbart"

# Inicjalizacja modelu Helsinki-NLP (MarianMT)
opus_model = pipeline("translation", model="Helsinki-NLP/opus-mt-pl-en")

# Inicjalizacja mBART
mbart_tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
mbart_model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

def translate_mbart(text: str) -> str:
    mbart_tokenizer.src_lang = "pl_PL"
    encoded = mbart_tokenizer(text, return_tensors="pt")
    generated_tokens = mbart_model.generate(
        **encoded,
        forced_bos_token_id=mbart_tokenizer.lang_code_to_id["en_XX"]
    )
    return mbart_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

@app.post("/translate")
def translate(request: TranslateRequest):
    text = request.text
    model = request.model.lower()

    if model == "opus":
        result = opus_model(text)[0]["translation_text"]
    elif model == "mbart":
        result = translate_mbart(text)
    else:
        return {"error": "Invalid model. Choose 'opus' or 'mbart'."}

    return {"translated_text": result}

@app.get("/")
def root():
    return {"message": "Translator API. Use POST /translate with model='opus' or 'mbart'."}
