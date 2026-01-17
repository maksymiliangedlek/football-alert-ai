import customtkinter as ctk
import threading
import time
from brain import generate_commentary
from notification import send_all_notifications
from find_team_id import get_team_id

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FootyBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Football Alert AI - Console")
        self.geometry("500x400")
        self.is_running = False

        self.label = ctk.CTkLabel(self, text="⚽ Football AI Monitor", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        combobox_var = ctk.StringVar(value="FC BARCELONA")
        self.team_entry = ctk.CTkComboBox(self,values=["FC BARCELONA", "REAL MADRID", "BAYERN MONACHIUM"],
                                    variable=combobox_var)
        self.team_entry.pack(pady=10, padx=20, fill="x")

        self.start_button = ctk.CTkButton(self, text="Uruchom monitoring", command=self.toggle_monitoring)
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=450, height=150)
        self.log_box.pack(pady=10)
        self.log_box.insert("0.0", "System gotowy. Wybierz druynę i kliknij start...\n")

    def log(self, text):
        self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.log_box.see("end")

    def toggle_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(text="Zatrzymaj", fg_color="red")
            self.log(f"Rozpoczynam śledzenie drużyny ID: {get_team_id(self.team_entry.get())}")
            threading.Thread(target=self.monitor_logic, daemon=True).start()
        else:
            self.is_running = False
            self.start_button.configure(text="Uruchom monitoring", fg_color="#1f538d")
            self.log("Monitoring zatrzymany.")

    def monitor_logic(self):
        """Tu trafi Twoja główna logika z main.py"""
        while self.is_running:
            # Tutaj będzie Twój get_live_match(team_id)
            # Na razie symulujemy działanie:
            self.log("Sprawdzam wynik...")
            fake_event = "Robert Lewandowski nie trafia sam na sam po czym idzie kontra i Mbappe strzela gola przewrotką w 92 minucie meczu z Barcelona po asyscie Rodrygo."
            score = "1:2"
    
            commentary = generate_commentary("FC Barcelona","Real Madrid",score,fake_event)
    
            send_all_notifications("GOOOL DLA Realu! ", commentary, score,fake_event)
            time.sleep(10) 

if __name__ == "__main__":
    app = FootyBotApp()
    app.mainloop()