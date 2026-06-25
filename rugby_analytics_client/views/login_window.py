import customtkinter as ctk

class MatchWindow(ctk.CTk):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        
        # Agganciamo il cambio dei dati alla nostra funzione di aggiornamento
        self.viewmodel.on_match_data_changed = self.aggiorna_dashboard

        # Configurazione Finestra di Gioco
        self.title("RugbyAnalytics Enterprise - Pannello Bordo Campo")
        self.geometry("600x450")
        self.resizable(False, False)

        # Configurazione Layout Griglia
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- SEZIONE SUPERIORE: TABELLONE PUNTEGGIO ---
        self.score_frame = ctk.CTkFrame(self, height=100)
        self.score_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.score_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.team_home_label = ctk.CTkLabel(self.score_frame, text="CASA", font=ctk.CTkFont(size=18, weight="bold"))
        self.team_home_label.grid(row=0, column=0, pady=10)

        self.score_label = ctk.CTkLabel(self.score_frame, text="00 - 00", font=ctk.CTkFont(size=28, weight="bold", text_color="#FFCC00"))
        self.score_label.grid(row=0, column=1, pady=10)

        self.team_away_label = ctk.CTkLabel(self.score_frame, text="OSPITI", font=ctk.CTkFont(size=18, weight="bold"))
        self.team_away_label.grid(row=0, column=2, pady=10)

        # --- SEZIONE INFERIORE: PULSANTIERA REGISTRAZIONE KPI ---
        self.kpi_title = ctk.CTkLabel(self, text="REGISTRAZIONE EVENTI LIVE", font=ctk.CTkFont(size=14, weight="bold", text_color="gray"))
        self.kpi_title.grid(row=1, column=0, columnspan=2, pady=(10, 5))

        # Bottone Meta (Esempio Giocatore ID #10)
        self.btn_meta = ctk.CTkButton(
            self, text="🏉 META (Casa)", 
            command=lambda: self.invia_evento("META", 10, 5, 0),
            fg_color="#2E7D32", hover_color="#1B5E20", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_meta.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Bottone Placcaggio (Esempio Giocatore ID #7)
        self.btn_placcaggio = ctk.CTkButton(
            self, text="💥 PLACCAGGIO", 
            command=lambda: self.invia_evento("PLACCAGGIO", 7),
            height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_placcaggio.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        # Bottone Touche Vinta (Esempio Giocatore ID #5)
        self.btn_touche = ctk.CTkButton(
            self, text="📐 TOUCHE VINTA", 
            command=lambda: self.invia_evento("TOUCHE", 5),
            fg_color="#1565C0", hover_color="#0D47A1", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_touche.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

    def invia_evento(self, tipo_kpi, giocatore_id, punti_casa=0, punti_ospiti=0):
        """Spedisce il pacchetto tramite il ViewModel e aggiorna il tabellone se necessario."""
        # Se l'evento cambia il punteggio (es. la Meta), aggiorna lo stato locale
        if punti_casa > 0 or punti_ospiti > 0:
            self.viewmodel.aggiorna_punteggio(punti_casa, punti_ospiti)
            
        # Invia al server tramite Socket
        self.viewmodel.registra_evento_kpi(tipo_kpi, giocatore_id)

    def aggiorna_dashboard(self):
        """Invocato quando i dati del ViewModel cambiano, rinfresca il tabellone dei punti."""
        nuovo_score = f"{self.viewmodel.punteggio_casa:02d} - {self.viewmodel.punteggio_ospiti:02d}"
        self.after(0, lambda: self.score_label.configure(text=nuovo_score))