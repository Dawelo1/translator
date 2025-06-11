# Cykl wdrażania aplikacji z wykorzystaniem obrazów Dockerowych na platformie Microsoft Azure

---

## **1. Przygotowanie środowiska aplikacji**

Proces wdrażania rozpoczyna się od przygotowania dwóch części aplikacji:

- **Backend (API)** — odpowiedzialny za logikę, obsługę żądań użytkowników i testy.  
- **Frontend (interfejs użytkownika)** — odpowiadający za wyświetlanie treści i interakcje użytkownika.

Dla obu części tworzy się osobne obrazy Docker, które zawierają wszystkie niezbędne zależności i konfigurację. Dzięki temu uzyskujemy przenośne środowisko uruchomieniowe niezależne od systemu operacyjnego. Obrazy są następnie wypychane do Docker Hub.

---

## **2. Przechowywanie obrazów kontenerowych**

Obrazy Dockerowe są przechowywane w **Docker Hub** — publicznym lub prywatnym rejestrze kontenerów. Docker Hub umożliwia łatwe udostępnianie i wersjonowanie obrazów.

Po ich przygotowaniu lokalnie, przesyła się je do Docker Hub, skąd są pobierane przez usługi w chmurze Microsoft Azure, takie jak **Azure Web App for Containers**, umożliwiające bezpośrednie wdrażanie aplikacji z użyciem wskazanych obrazów.

---

## **3. Konfiguracja usługi Azure Web App for Containers**

Do uruchomienia aplikacji bez zarządzania infrastrukturą służy **Azure Web App for Containers**. Tworzone są dwa niezależne Web Appy:

- **Web App dla API** — obsługuje logikę aplikacji oraz żądania HTTP/HTTPS.
- **Web App dla frontendu** — serwuje interfejs użytkownika jako aplikację webową.

Podczas konfiguracji wskazuje się nazwę obrazu i jego wersję (tag) z Docker Huba. Obie aplikacje są publicznie dostępne, co upraszcza konfigurację i minimalizuje zużycie zasobów.

---

## **4. Konfiguracja środowiska aplikacji**

Ustawiane są zmienne środowiskowe, które umożliwiają poprawne działanie aplikacji, m.in.:

- adresy URL do usług (np. baza danych),
- klucze API,
- ścieżki dostępu.

Pozwala to zarządzać konfiguracją bez ingerencji w kod źródłowy.

---

## **5. Udostępnienie aplikacji użytkownikom**

Po wdrożeniu aplikacja staje się dostępna pod publicznymi adresami URL. Azure umożliwia również:

- przypisanie własnej domeny,
- aktywację certyfikatów SSL (HTTPS).

W projekcie nie zastosowano tej opcji z uwagi na ograniczenia subskrypcji.

---

## **6. Problemy wynikające z subskrypcji na Azure**

W związku z ograniczoną subskrypcją **Azure for Students**, aplikacja nie może być uruchomiona na stałe.

- Obraz API waży około **6 GB**, ze względu na wbudowane modele językowe.
- Po godzinie bezczynności aplikacje są automatycznie zatrzymywane.
- Uruchomienie back-endu trwa długo, co wpływa na wygodę użytkowania.

---

