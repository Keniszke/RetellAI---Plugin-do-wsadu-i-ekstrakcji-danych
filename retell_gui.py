# interfejs graficzny do zarządzania skryptami połączeń i eksportu
# biblioteki GUI tkinter oraz dodatkowe elementy
import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
from dotenv import set_key
from call_numbers import run_call_numbers
from export_data import run_export_data


def log(msg):
    # wyświetla komunikat w polu tekstowym, blokując edycję
    txt.configure(state="normal")
    txt.insert(tk.END, msg + "\n")
    txt.see(tk.END)
    txt.configure(state="disabled")


def save_api():
    # pobiera wartość z pola tekstowego i zapisuje do pliku .env
    # oraz ustawia zmienną środowiskową
    key = entry.get().strip()

    if not key:
        messagebox.showwarning("Błąd", "API Key pusty")
        return

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    set_key(dotenv_path, "API_KEY", key)

    os.environ["API_KEY"] = key

    log("API Key zapisany")


def run_calls():
    # wywołuje moduł odpowiedzialny za nawiązywanie połączeń
    # dry_run=True oznacza symulację bez rzeczywistych połączeń
    log("Start połączeń...")

    try:
        run_call_numbers(dry_run=True)
        log("Połączenia zakończone")
    except Exception as e:
        log(f"Błąd: {e}")


def run_export():
    # uruchamia funkcję eksportującą dane do pliku
    log("Eksport danych...")

    try:
        run_export_data()
        log("Eksport zakończony")
    except Exception as e:
        log(f"Błąd: {e}")


# konfiguracja głównego okna aplikacji
root = tk.Tk()
root.title("RetellAI Manager")
root.geometry("800x500")

# ramka do ustawienia klucza API
frame_api = tk.Frame(root)
frame_api.pack(pady=10)

tk.Label(frame_api, text="API Key").pack(side=tk.LEFT)

entry = tk.Entry(frame_api, width=50)
entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_api, text="Zapisz API", command=save_api).pack(side=tk.LEFT)

frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Uruchom połączenia", width=25, command=run_calls).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Eksportuj dane", width=25, command=run_export).grid(row=0, column=1, padx=10)

txt = scrolledtext.ScrolledText(root, width=95, height=25, state="disabled")
txt.pack(pady=10)

root.mainloop()