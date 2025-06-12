# 4. Opis danych

**Dane wejściowe:**
- Tekst w języku polskim (mogą to być pojedyncze zdania lub dłuższe fragmenty).
- Możliwość wczytania plików tekstowych do przetwarzania.

**Dane wyjściowe:**
- Tłumaczenia wyłącznie na język angielski.

W projekcie wykorzystujemy dwa gotowe, wytrenowane wcześniej modele tłumaczeniowe: `mbart-50` i `opus-mt`. Modele te zostały opracowane odpowiednio przez Facebook AI (obecnie Meta AI) oraz zespół Helsinki-NLP i były trenowane na dużych, wielojęzycznych korpusach takich jak **Europarl** i **Tatoeba**.

Porównujemy jakości tłumaczeń generowanych przez te modele na wspólnym zbiorze danych wejściowych.
