# 3. Przegląd literatury

Projekt Translator bazuje na najnowszych osiągnięciach w dziedzinie tłumaczenia maszynowego (Machine Translation, MT), w szczególności tłumaczenia neuronowego (Neural Machine Translation, NMT). Wykorzystuje gotowe modele udostępnione przez społeczność open-source za pośrednictwem platformy Hugging Face oraz implementacje sieci neuronowych w PyTorch.

**Główne źródła teoretyczne i narzędziowe:**

- **Klein et al. (2017), “OpenNMT: Open-Source Toolkit for Neural Machine Translation”**  
  → Artykuł opisuje architekturę OpenNMT, jednego z pierwszych otwartych frameworków do tłumaczenia neuronowego. OpenNMT umożliwia budowanie modeli typu encoder-decoder, obsługujących tłumaczenie sekwencji na sekwencję, często wykorzystywane w zadaniach NMT.

- **Hugging Face – Transformers i modele tłumaczeniowe**  
  → Projekt korzysta z gotowych modeli udostępnionych przez społeczność:  
  - [`Helsinki-NLP/opus-mt-pl-en`](https://huggingface.co/Helsinki-NLP/opus-mt-pl-en) — model tłumaczenia PL→EN oparty na MarianMT, wytrenowany na zbiorach Europarl, Tatoeba i innych korpusach z projektu OPUS.  
  - [`facebook/mbart-large-50-many-to-many-mmt`](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt) — wielojęzyczny model seq2seq MBART-50 obsługujący 50 języków i wspierający tłumaczenia w różnych kierunkach.

- **PyTorch**  
  → Główna biblioteka do implementacji i uruchamiania modeli MBART. Zapewnia niskopoziomowy dostęp do GPU i kontrolę nad modelem.

- **Transformers (Hugging Face)**  
  → Wysokopoziomowa biblioteka ułatwiająca pracę z nowoczesnymi modelami NLP. W projekcie wykorzystywana do ładowania modeli, tokenizacji oraz generowania tłumaczeń.

- **NLTK (Natural Language Toolkit)**  
  → Biblioteka służąca do przetwarzania języka naturalnego. W projekcie używana do dzielenia tekstu na zdania przed ich tłumaczeniem.

**Dodatkowe źródła i inspiracje:**

- Dokumentacja Hugging Face: https://huggingface.co/docs  
- Dokumentacja PyTorch: https://pytorch.org/docs  
- Dokumentacja OpenNMT: https://opennmt.net  
- Dokumentacja BLEU (sacreBLEU): https://github.com/mjpost/sacrebleu  

Projekt opiera się na podejściu porównawczym — analiza wyników tłumaczenia uzyskanych przez różne modele umożliwia lepsze zrozumienie ich zalet, ograniczeń i kontekstów użycia.
