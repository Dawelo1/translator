from datasets import load_dataset
from utils.translation_utils import init_models, evaluate_models_on_dataset
import os

def save_report(opus_bleu, mbart_bleu):
    os.makedirs("reports", exist_ok=True)
    with open("reports/evaluation_report.md", "w", encoding="utf-8") as f:
        f.write("# Raport ewaluacji modeli tłumaczenia PL->EN\n\n")
        f.write(f"## Wyniki BLEU:\n\n")
        f.write(f"- Opus-MT: **{opus_bleu:.2f}**\n")
        f.write(f"- mBART-50: **{mbart_bleu:.2f}**\n\n")
        f.write("Test wykonano na 100 zdaniach z zestawu WMT14.\n")

def main():
    print("Ładowanie danych testowych WMT14...")
    dataset = load_dataset("wmt14", "pl-en", split="test[:100]")

    print("Inicjalizacja modeli...")
    opus_model, mbart_tokenizer, mbart_model = init_models()

    print("Rozpoczynamy ewaluację...")
    opus_bleu, mbart_bleu = evaluate_models_on_dataset(dataset, opus_model, mbart_tokenizer, mbart_model)

    print(f"Opus-MT BLEU: {opus_bleu:.2f}")
    print(f"mBART BLEU: {mbart_bleu:.2f}")

    save_report(opus_bleu, mbart_bleu)
    print("Raport zapisany w reports/evaluation_report.md")

if __name__ == "__main__":
    main()
