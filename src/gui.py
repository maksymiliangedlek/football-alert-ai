import customtkinter as ctk
import threading
import time
from brain import generate_commentary
from notification import send_all_notifications
from find_team_id import get_team_id
from football_api import get_live_match_data, get_match_events

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FootyBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Football Alert AI - Console")
        self.geometry("600x500")
        
        self.is_running = False
        self.current_thread = None
        self.monitored_team_name = "" 
        self.team_id = 0
        self.last_event_id = None


        self.label = ctk.CTkLabel(self, text="⚽ Football AI Monitor", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        self.team_entry = ctk.CTkComboBox(
            self, 
            values=["FC BARCELONA","Atletico Madrid", "REAL MADRID", "BAYERN MONACHIUM"],
            command=self.on_team_change
        )
        self.team_entry.set("Atletico Madrid")
        self.team_entry.pack(pady=10, padx=20, fill="x")

        self.start_button = ctk.CTkButton(self, text="Uruchom monitoring", command=self.toggle_monitoring)
        self.start_button.pack(pady=20)

        self.log_box = ctk.CTkTextbox(self, width=550, height=250)
        self.log_box.pack(pady=10)
        self.log("System gotowy. Wybierz drużynę i kliknij start...")

    def log(self, text):
        def _log():
            self.log_box.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
            self.log_box.see("end")
        self.after(0, _log)

    def on_team_change(self, choice):
        if self.is_running:
            self.log(f"⚠️ Zmiana na {choice}. Restartowanie monitoringu...")
            self.stop_monitoring()
            
    def safe_stop_monitoring(self):
        def _stop():
            self.is_running = False
            self.start_button.configure(text="Uruchom monitoring", fg_color="#1f538d")
            self.log("🛑 Zatrzymano.")
        self.after(0, _stop)


    def toggle_monitoring(self):
        if not self.is_running:
            self.is_running = True
            self.monitored_team_name = self.team_entry.get()
            self.start_button.configure(text="Zatrzymaj", fg_color="red")
            self.log(f"Rozpoczynam śledzenie drużyny ID: {get_team_id(self.team_entry.get())}")
            threading.Thread(target=self.monitor_logic, daemon=True).start()
        else:
            self.is_running = False
            self.start_button.configure(text="Uruchom monitoring", fg_color="#1f538d")
            self.log("Monitoring zatrzymany.")

    def monitor_logic(self):
        team_id = get_team_id(self.monitored_team_name)
        target_team_name = self.monitored_team_name 
        
        if not team_id:
            self.log("❌ Błąd: Nie znaleziono ID drużyny.")
            self.safe_stop_monitoring()
            return

        self.log(f"🟢 Wątek aktywny. Cel: {target_team_name} (ID: {team_id})")
        
        while self.is_running:
            try:
                match_data = get_live_match_data(team_id)
                
                if match_data:
                    fixture_id = match_data["fixture"]["id"]
                    home_team = match_data['teams']['home']['name']
                    away_team = match_data['teams']['away']['name']
                    score = f"{match_data['goals']['home']}:{match_data['goals']['away']}"
                    
                    self.log(f"✅ Pobrano mecz: {home_team} vs {away_team} ({score})")
                    print(f"✅ Pobrano mecz: {home_team} vs {away_team} ({score})")
                    events = get_match_events(fixture_id)
                    
                    if events:
                        event = events[-1]
                        event_id = f"{event['type']}_{event.get('detail','')}_{event.get('player',{}).get('name','Nieznany')}_{event['time']['elapsed']}"

                    
                        if event_id == self.last_event_id:
                            self.log("🔁 Event już był obsłużony, pomijam.")
                            time.sleep(5)
                            continue
                        self.last_event_id = event_id

                        p_name = event.get('player', {}).get('name') if event.get('player') else "Nieznany"
                        detail = event.get('detail', 'Akcja')
                        minute = event['time']['elapsed']
                        
                        event_desc = f"{event['type']}: {detail} ({p_name}, {minute} min)"
                        self.log(f"🔥 Znaleziono event: {event_desc}")
                        self.log("🧠 Generuję komentarz AI...")
                        
                        commentary = generate_commentary(
                            home_team, away_team, target_team_name, score, event_desc
                        )
                        
                        self.log(f"💬 AI: {commentary}")
                        send_all_notifications(f"COŚ SIĘ STAŁO W {home_team} vs {away_team}", commentary, score, event_desc)

                        time.sleep(5)
                    else:
                        print("pusta")
                        self.log("ℹ️ Mecz pobrany, ale lista zdarzeń jest pusta.")
                        time.sleep(5)
                for _ in range(120):
                    if not self.is_running: break
                    time.sleep(1)
                    
            except Exception as e:
                self.log(f"⚠️ Błąd: {e}")
                time.sleep(5)

        self.log("💀 Wątek zakończył pracę.")
if __name__ == "__main__":
    app = FootyBotApp()
    app.mainloop()