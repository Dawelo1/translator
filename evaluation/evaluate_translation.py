import os
import json
import random
import argparse
from datasets import load_dataset, Dataset
from utils.translation_utils import init_models, evaluate_models_on_dataset

def save_report(opus_bleu, mbart_bleu):
    os.makedirs("reports", exist_ok=True)
    with open("reports/evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("# Raport ewaluacji modeli tłumaczenia PL->EN\n\n")
        f.write(f"## Wyniki BLEU:\n\n")
        f.write(f"- Opus-MT: **{opus_bleu:.2f}**\n")
        f.write(f"- mBART-50: **{mbart_bleu:.2f}**\n\n")
        f.write("Test wykonano na wybranych zdaniach z zestawu danych opus_books lub pliku manualnego.\n")

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

def save_test_data(dataset):
    os.makedirs("data", exist_ok=True)
    data = [{"pl": ex["translation"]["pl"], "en": ex["translation"]["en"]} for ex in dataset]
    with open("data/test_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Testowe dane zapisane w data/test_data.json")

def load_manual_dataset(path="data/test_data_manual.json"):
    print(f"Wczytywanie danych ręcznych z: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Konwertuj na Hugging Face Dataset ze strukturą {"translation": {"pl": ..., "en": ...}}
    formatted = [{"translation": {"pl": item["pl"], "en": item["en"]}} for item in data]
    return Dataset.from_list(formatted)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual", action="store_true", help="Użyj danych z pliku data/test_data_manual.json")
    args = parser.parse_args()

    if args.manual:
        dataset = load_manual_dataset()
    else:
        print("Ładowanie pełnego zbioru treningowego opus_books...")
        full_dataset = load_dataset("opus_books", "en-pl", split="train")
        print("Losowanie 50 przykładów...")
        dataset = random.sample(list(full_dataset), 50)
        print("Zapisywanie testowych danych do data/test_data.json...")
        save_test_data(dataset)

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
