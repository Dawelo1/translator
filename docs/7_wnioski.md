# 7. Wnioski

Projekt **Translator** potwierdza, że tłumaczenie tekstów z języka polskiego na angielski może być skutecznie realizowane lokalnie przy użyciu gotowych modeli neuronowych, bez potrzeby korzystania z komercyjnych usług chmurowych.

**Najważniejsze wnioski:**
- Aplikacja działa stabilnie i wydajnie, a dzięki konteneryzacji z użyciem Dockera możliwe jest szybkie uruchomienie zarówno lokalnie, jak i w chmurze (np. Microsoft Azure).
- Zastosowano dwa gotowe, otwarte modele tłumaczeniowe:
  - **Opus-MT** (`Helsinki-NLP/opus-mt-pl-en`) — lekki i szybki model, bardzo dobrze radzi sobie z prostymi, technicznymi tekstami. Idealny do zastosowań w środowiskach o ograniczonych zasobach.
  - **mBART-50** (`facebook/mbart-large-50-many-to-many-mmt`) — większy i bardziej zaawansowany model, oparty na architekturze seq2seq z pretreningiem. Zdecydowanie lepiej radzi sobie z kontekstem, niuansami językowymi i bardziej naturalnym stylem tłumaczenia, kosztem większego zapotrzebowania na zasoby obliczeniowe.

- W bezpośrednim porównaniu:  
  - **Opus-MT** oferuje szybsze odpowiedzi i mniejsze zużycie pamięci.  
  - **mBART-50** generuje bardziej naturalne i płynne tłumaczenia, szczególnie przy dłuższych i bardziej złożonych tekstach.

- Możliwości dalszego rozwoju obejmują:  
  - dodanie opcji logowania i oceny wyników,
  - rozbudowę interfejsu graficznego,
  - integrację z bazami danych lub platformami edukacyjnymi.

Projekt ma wartość edukacyjną oraz potencjał do praktycznego wykorzystania jako lekkie narzędzie do lokalnego tłumaczenia tekstów specjalistycznych lub prywatnych.
