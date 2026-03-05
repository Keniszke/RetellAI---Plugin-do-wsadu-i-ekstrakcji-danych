
Biblioteki:

- **requests** – komunikacja z API  
- **pandas** – przetwarzanie danych i DataFrame  
- **openpyxl** – tworzenie i stylizacja plików Excel  
- **python-dotenv** – wczytywanie zmiennych środowiskowych z `.env`  

--------------------------------------------------

## Instalacja Bibliotek

## 1. Otwórz:
install.bat

## Lub wpisz w konsoli następujące komendy: 
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


## 2. Otwórz konsole w folderze RetellAI
## 3. Uruchom skrypt retell_gui:
venv\Scripts\activate (jeśli nie masz jeszcze aktywowanego venv)
python retell_gui.py

## 4. Wklej API w oknie API_KEY, wczytaj
--------------------------------------------------


--------------------------------------------------
## Jak używać?

## 1. Do folderu surveys_to_call wrzuć plik o nazwie numbers_to_call.csv (UTF-8)
numbers_to_call  musi mieć identyczną tabelę, żeby działało

## 2. W panelu retell_gui wciśnij "Uruchom Połączenia"
W tym momencie wykonuje się batch call do wszystkich numerów na liście w pliku numbers_to_call
Po zakończeniu w logu pojawi się napis "Połączenia zakończone"

## 3. Wciśnij "Eksportuj Dane"
Tutaj generuje się plik z zebranymi danymi z rozmowy w formacie .CSV UTF-8

## 4. Ciesz sie mniejszym zrzędzeniem działu infolinii

## Pliki z danymi musza być w formacie .CSV UTF-8
--------------------------------------------------