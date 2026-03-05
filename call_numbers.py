import os
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime

## Skrypt do inicjowania połączeń telefonicznych na podstawie numerów z pliku CSV
def run_call_numbers(dry_run=True):

    ## Kluczyk API
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("Nie znaleziono klucza API w pliku .env")

    ## Ścieżki do plików i folderów
    script_dir = os.path.dirname(os.path.abspath(__file__))
    SURVEYS_FOLDER = os.path.join(script_dir, "surveys_to_call")
    INPUT_FILE = os.path.join(SURVEYS_FOLDER, "numbers_to_call.csv")
    EXPORT_FOLDER = os.path.join(script_dir, "exported_calls")
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    CALLS_LOG_FILE = os.path.join(EXPORT_FOLDER, "last_calls.csv")

    ## Wczytaj CSV UTF-8 z BOM
    df = pd.read_csv(INPUT_FILE, encoding="utf-8-sig")

    if "phone_number" not in df.columns:
        raise ValueError("Brak kolumny 'phone_number' w pliku wejściowym")

    ## Uzupełnij brakujące kolumny i ustaw typy danych
    if "attempts" not in df.columns:
        df["attempts"] = 0
    if "called_successfully" not in df.columns:
        df["called_successfully"] = False

    df["attempts"] = pd.to_numeric(df["attempts"].fillna(0), errors="coerce").fillna(0).astype(int)
    df["called_successfully"] = df["called_successfully"].fillna(False)

    ## Filtruj numery do dzwonienia
    df_to_call = df[(df["attempts"] < 2) & (df["called_successfully"] == False)].copy()
    if df_to_call.empty:
        print("Brak numerów do dzwonienia – wszystkie osiągnęły limit prób lub już zostały połączone.")
        return

    ## Przygotuj nagłówki i URL do API
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    url_create_call = "https://api.retellai.com/v2/calls"

    ## Funkcja aktualizacji prób i statusu połączenia
    def update_attempts(number: str, success: bool):
        mask = df["phone_number"] == number
        df.loc[mask, "attempts"] = df.loc[mask, "attempts"] + 1
        if success:
            df.loc[mask, "called_successfully"] = True

    ## Funkcja wysyłania połączenia
    def send_call_request(number: str):
        if dry_run:
            class MockResponse:
                def json(self):
                    return {"call_id": f"SIM-{number}"}
                def raise_for_status(self):
                    pass
            return MockResponse()
        else:
            payload = {"phone_number": number, "call_type": "outbound"}
            response = requests.post(url_create_call, json=payload, headers=headers)
            response.raise_for_status()
            return response

    ## Wysyłaj połączenia i aktualizuj statusy
    executed_call_ids = []
    for number in df_to_call["phone_number"]:
        try:
            response = send_call_request(number)
            data = response.json()
            call_id = data.get("call_id", f"SIM-{number}")
            executed_call_ids.append(call_id)
            print(f"✅ Połączenie z {number} zainicjowane: {call_id}")
            update_attempts(number, success=True)
        except Exception as e:
            print(f"❌ Błąd przy numerze {number}: {e}")
            update_attempts(number, success=False)

    ## Zapisz zaktualizowany DataFrame do CSV
    df.to_csv(INPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ Zaktualizowany stan zapisany w {INPUT_FILE}")

    ## Zapisz nowe ID połączeń do logu
    if os.path.exists(CALLS_LOG_FILE):
        df_log = pd.read_csv(CALLS_LOG_FILE, encoding="utf-8-sig")
    else:
        df_log = pd.DataFrame(columns=["call_id"])

    df_log = pd.concat([df_log, pd.DataFrame({"call_id": executed_call_ids})], ignore_index=True)
    df_log.drop_duplicates(subset=["call_id"], inplace=True)
    df_log.to_csv(CALLS_LOG_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ Zapis nowych ID połączeń w {CALLS_LOG_FILE}")

## Uruchom skrypt
if __name__ == "__main__":
    run_call_numbers(dry_run=True)