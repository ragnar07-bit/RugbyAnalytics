import customtkinter as ctk

class MatchWindow(ctk.CTk):
    def __init__(self, viewmodel):
        super().__init__()
        self.viewmodel = viewmodel
        
        # Aggancio della callback di stato
        self.viewmodel.on_match_data_changed = self.aggiorna_dashboard

        # Configurazione Finestra di Gioco
        self.title("RugbyAnalytics Enterprise - Pannello Bordo Campo")
        self.geometry("650x500")
        self.resizable(False, False)

        # Configurazione Layout Griglia (2 Colonne bilanciate)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- SEZIONE SUPERIORE: TABELLONE PUNTEGGIO ---
        self.score_frame = ctk.CTkFrame(self, height=100)
        self.score_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.score_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.team_home_label = ctk.CTkLabel(self.score_frame, text="CASA", font=ctk.CTkFont(size=18, weight="bold"))
        self.team_home_label.grid(row=0, column=0, pady=15)

        self.score_label = ctk.CTkLabel(
            self.score_frame, text="00 - 00", 
            font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFCC00"
        )
        self.score_label.grid(row=0, column=1, pady=15)

        self.team_away_label = ctk.CTkLabel(self.score_frame, text="OSPITI", font=ctk.CTkFont(size=18, weight="bold"))
        self.team_away_label.grid(row=0, column=2, pady=15)

        # --- TITOLO SEZIONE LIVE ---
        self.kpi_title = ctk.CTkLabel(self, text="REGISTRAZIONE EVENTI LIVE", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")
        self.kpi_title.grid(row=1, column=0, columnspan=2, pady=(5, 15))

        # --- COLONNA 1: AZIONI CASA (A Sinistra) ---
        self.btn_meta_casa = ctk.CTkButton(
            self, text="🏉 META (Casa)", 
            command=lambda: self.invia_evento("META_CASA", 10, punti_casa=5),
            fg_color="#2E7D32", hover_color="#1B5E20", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_meta_casa.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="nsew")

        self.btn_touche_vinta = ctk.CTkButton(
            self, text="📐 TOUCHE VINTA", 
            command=lambda: self.invia_evento("TOUCHE_VINTA", 5),
            fg_color="#1565C0", hover_color="#0D47A1", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_touche_vinta.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="nsew")

        # --- COLONNA 2: AZIONI OSPITI / ERRORI (A Destra) ---
        self.btn_meta_ospiti = ctk.CTkButton(
            self, text="❌ META SUBITA (Ospiti)", 
            command=lambda: self.invia_evento("META_OSPITI", 0, punti_ospiti=5),
            fg_color="#C62828", hover_color="#9E1B1B", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_meta_ospiti.grid(row=2, column=1, padx=(10, 20), pady=10, sticky="nsew")

        self.btn_touche_persa = ctk.CTkButton(
            self, text="⚠️ TOUCHE PERSA", 
            command=lambda: self.invia_evento("TOUCHE_PERSA", 5),
            fg_color="#EF6C00", hover_color="#D84315", height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_touche_persa.grid(row=3, column=1, padx=(10, 20), pady=10, sticky="nsew")

        # --- AZIONI GENERICHE (Su tutta la riga) ---
        self.btn_placcaggio = ctk.CTkButton(
            self, text="💥 PLACCAGGIO EFFETTUATO", 
            command=lambda: self.invia_evento("PLACCAGGIO", 7),
            height=50, font=ctk.CTkFont(weight="bold")
        )
        self.btn_placcaggio.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    def invia_evento(self, tipo_kpi, giocatore_id, punti_casa=0, punti_ospiti=0):
        """Aggiorna la grafica locale in caso di punti e delega l'invio di rete al ViewModel."""
        if punti_casa > 0 or punti_ospiti > 0:
            self.viewmodel.aggiorna_punteggio(punti_casa, punti_ospiti)
            
        self.viewmodel.registra_evento_kpi(tipo_kpi, giocatore_id)

    def aggiorna_dashboard(self):
        """Rinfresca il testo del tabellone dei punti usando un thread-safe after."""
        nuovo_score = f"{self.viewmodel.punteggio_casa:02d} - {self.viewmodel.punteggio_ospiti:02d}"
        self.after(0, lambda: self.score_label.configure(text=nuovo_score))