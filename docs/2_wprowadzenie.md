# 2. Wprowadzenie

W ostatnich latach narzędzia do tłumaczenia maszynowego oparte na głębokich sieciach neuronowych znacząco poprawiły jakość automatycznej translacji tekstów. Projekt **Translator** powstał jako próba stworzenia samodzielnej aplikacji umożliwiającej tłumaczenie offline z języka **polskiego na angielski**, bez potrzeby korzystania z komercyjnych usług chmurowych takich jak Google Translate.

## Cel projektu

Główne cele projektu to:

- stworzenie aplikacji tłumaczącej z **polskiego na angielski** (jednokierunkowo),
- porównanie działania dwóch gotowych modeli tłumaczeniowych typu encoder-decoder:
  - `Helsinki-NLP/opus-mt-pl-en`,
  - `facebook/mbart-large-50-many-to-many-mmt`,
- zapewnienie prostego **API** oraz graficznego interfejsu **GUI (Streamlit)** do wykonywania tłumaczeń,
- wdrożenie aplikacji jako usługi chmurowej w **Microsoft Azure** (z wykorzystaniem kontenerów Docker).

Lokalne uruchomienie aplikacji służy głównie jako środowisko testowe i deweloperskie. Finalnym celem projektu jest udostępnienie systemu jako usługi webowej dla użytkowników zewnętrznych.

---

## Modele tłumaczeniowe

Projekt wykorzystuje dwa różne podejścia do tłumaczenia:

1. **Opus-MT (`opus-mt-pl-en`)** — lekki, szybki model oparty na architekturze MarianMT, przeznaczony do prostych zastosowań produkcyjnych.
2. **MBart-50 (`mbart-large-50-many-to-many-mmt`)** — większy, bardziej złożony model przystosowany do wielu języków, z lepszym rozumieniem kontekstu i większą dokładnością.

Oba modele są pretrenowane i dostępne za darmo poprzez platformę Hugging Face.

---

## Architektura i funkcjonalności

Główne komponenty implementacyjne:

- **Inicjalizacja modeli**:
  Modele są ładowane z Hugging Face i przygotowywane do działania na GPU (jeśli dostępny) lub CPU. W przypadku `mbart-50` dodatkowo inicjalizowany jest tokenizer z ustawionym językiem źródłowym jako `pl_PL`.

- **Tłumaczenie tekstu**:
  Tekst wejściowy dzielony jest na zdania za pomocą NLTK (`sent_tokenize`) i tłumaczony sekwencyjnie. Dla `opus-mt` każde zdanie jest tłumaczone niezależnie, natomiast `mbart-50` generuje tłumaczenie dla całego bloku tekstu.

- **Ewaluacja BLEU**:
  Funkcja `evaluate_models_on_dataset()` wykorzystuje bibliotekę `evaluate` i metrykę **sacreBLEU**, aby ocenić jakość tłumaczeń w odniesieniu do zestawu referencyjnych tłumaczeń. Oba modele są testowane na tych samych danych wejściowych i wynik porównywany.

---

## Wykorzystane biblioteki

- `transformers` – obsługa modeli `opus-mt` i `mbart-50`,
- `nltk` – tokenizacja zdań,
- `evaluate` – ewaluacja jakości tłumaczeń za pomocą metryk (BLEU),
- `torch` – obsługa GPU/CPU i działania modeli PyTorch,
- `pipeline` – uproszczone API dla translacji.

---

W kolejnych sekcjach znajdziesz szczegółowy opis danych, metody uruchamiania aplikacji, proces wdrożenia oraz wyniki porównania jakości tłumaczeń.

