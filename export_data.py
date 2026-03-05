import os
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

## Skrypt do eksportowania danych z połączeń telefonicznych do pliku CSV
def run_export_data(dry_run=True):

    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    if not API_KEY and not dry_run:
        raise ValueError("Nie znaleziono klucza API w pliku .env")

    ## Ścieżki do plików i folderów

    script_dir = os.path.dirname(os.path.abspath(__file__))
    EXPORT_FOLDER = os.path.join(script_dir, "exported_calls")
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    CALLS_LOG_FILE = os.path.join(EXPORT_FOLDER, "last_calls.csv")

    if not os.path.exists(CALLS_LOG_FILE):
        print("❌ Brak last_calls.csv – najpierw wykonaj połączenia.")
        return

    ## Wczytaj log połączeń

    df_calls = pd.read_csv(CALLS_LOG_FILE, encoding="utf-8-sig")

    if "call_id" not in df_calls.columns:
        print("❌ last_calls.csv nie zawiera kolumny call_id")
        return

    ## Przygotuj nagłówki do API

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    results = []

    for call_id in df_calls["call_id"]:

        try:

            if dry_run:

                collected = {
                    "previous_node": "Start",
                    "current_node": "Survey1",
                    "surveyScore": 10,
                    "surveyConsent": True,
                    "isStatisfied": True,
                    "satisfactionCause": "Good service",
                    "userIdentity": "TestUser"
                }

            else:

                url = f"https://api.retellai.com/v2/get-call/{call_id}"

                response = requests.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                collected = data.get("collected_dynamic_variables", {})

            results.append({
                "call_id": call_id,
                "previous_node": collected.get("previous_node", ""),
                "current_node": collected.get("current_node", ""),
                "surveyScore": collected.get("surveyScore", ""),
                "surveyConsent": collected.get("surveyConsent", ""),
                "isStatisfied": collected.get("isStatisfied", ""),
                "satisfactionCause": collected.get("satisfactionCause", ""),
                "userIdentity": collected.get("userIdentity", "")
            })

        except Exception as e:

            print(f"❌ Błąd dla {call_id}: {e}")

    if not results:
        print("❌ Brak danych do eksportu")
        return

    ## Zapisz wyniki do nowego pliku CSV

    df_export = pd.DataFrame(results)

    OUTPUT_FILE = f"FUP_NPS_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    output_path = os.path.join(EXPORT_FOLDER, OUTPUT_FILE)

    df_export.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ FUP_NPS zapisany: {output_path}")

## Uruchom skrypt
if __name__ == "__main__":
    run_export_data(dry_run=True)