import torch
from transformers import pipeline, MBartForConditionalGeneration, MBart50TokenizerFast
from nltk.tokenize import sent_tokenize
import nltk
from datasets import load_metric

nltk.download('punkt')

# Inicjalizacja modeli
def init_models():
    device = 0 if torch.cuda.is_available() else -1
    opus_model = pipeline("translation", model="Helsinki-NLP/opus-mt-pl-en", device=device)

    mbart_tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    mbart_model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    mbart_model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    return opus_model, mbart_tokenizer, mbart_model

def translate_opus(text, opus_model):
    sentences = sent_tokenize(text, language='polish')
    translations = []
    for sent in sentences:
        result = opus_model(sent)[0]['translation_text']
        translations.append(result)
    return " ".join(translations)

def translate_mbart(text, mbart_tokenizer, mbart_model):
    mbart_tokenizer.src_lang = "pl_PL"
    device = next(mbart_model.parameters()).device
    encoded = mbart_tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    generated_tokens = mbart_model.generate(
        **encoded,
        forced_bos_token_id=mbart_tokenizer.lang_code_to_id["en_XX"],
        max_length=512
    )
    return mbart_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

def evaluate_models_on_dataset(dataset, opus_model, mbart_tokenizer, mbart_model):
    bleu_metric = load_metric("sacrebleu")

    opus_preds = []
    mbart_preds = []
    references = []

    for example in dataset:
        pl_text = example["translation"]["pl"]
        en_ref = example["translation"]["en"]

        opus_trans = translate_opus(pl_text, opus_model).lower().split()
        mbart_trans = translate_mbart(pl_text, mbart_tokenizer, mbart_model).lower().split()
        ref_tokens = en_ref.lower().split()

        opus_preds.append(opus_trans)
        mbart_preds.append(mbart_trans)
        references.append([ref_tokens])

    opus_score = bleu_metric.compute(predictions=opus_preds, references=references)
    mbart_score = bleu_metric.compute(predictions=mbart_preds, references=references)

    return opus_score['score'], mbart_score['score']
