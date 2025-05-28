import os
import json
from datasets import Dataset
from utils.translation_utils import init_models, evaluate_models_on_dataset

def save_report(opus_bleu, mbart_bleu):
    os.makedirs("reports", exist_ok=True)
    with open("reports/evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("# Raport ewaluacji modeli tłumaczenia PL->EN\n\n")
        f.write("## Wyniki BLEU:\n\n")
        f.write(f"- Opus-MT: **{opus_bleu:.2f}**\n")
        f.write(f"- mBART-50: **{mbart_bleu:.2f}**\n\n")
        f.write("Test wykonano na danych z pliku manualnego: `data/test_data_manual.json`.\n")

def save_data_json(dataset, opus_preds, mbart_preds):
    os.makedirs("reports", exist_ok=True)
    data = []
    for example, opus_out, mbart_out in zip(dataset, opus_preds, mbart_preds):
        data.append({
            "source_pl": example["translation"]["pl"],
            "reference_en": example["translation"]["en"],
            "opus_mt": opus_out,
            "mbart": mbart_out
        })
    with open("reports/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Dane zapisane w reports/data.json")

def load_manual_dataset(path="data/test_data_manual.json"):
    print(f"Wczytywanie danych ręcznych z: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    formatted = [{"translation": {"pl": item["pl"], "en": item["en"]}} for item in data]
    return Dataset.from_list(formatted)

def main():
    dataset = load_manual_dataset()

    print(f"Przykładowy rekord testowy: {dataset[0]}")

    print("Inicjalizacja modeli...")
    opus_model, mbart_tokenizer, mbart_model = init_models()

    print("Rozpoczynamy ewaluację...")
    opus_bleu, mbart_bleu, opus_preds, mbart_preds = evaluate_models_on_dataset(
        dataset, opus_model, mbart_tokenizer, mbart_model, return_predictions=True
    )

    print(f"Opus-MT BLEU: {opus_bleu:.2f}")
    print(f"mBART BLEU: {mbart_bleu:.2f}")

    save_report(opus_bleu, mbart_bleu)
    save_data_json(dataset, opus_preds, mbart_preds)

    print("Raport zapisany w reports/evaluation_report.md")

if __name__ == "__main__":
    main()
