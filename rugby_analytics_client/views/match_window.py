import customtkinter as ctk

class LoginWindow(ctk.CTk):
    def __init__(self, viewmodel, on_authenticated_callback):
        super().__init__()
        self.viewmodel = viewmodel
        self.on_authenticated_callback = on_authenticated_callback
        
        # Agganciamo le funzioni del ViewModel alle funzioni grafiche della Window
        self.viewmodel.on_status_changed = self.aggiorna_stato
        self.viewmodel.on_login_success = self.gestisci_successo

        # Configurazione Finestra di Sistema
        self.title("RugbyAnalytics Enterprise - Login")
        self.geometry("400x520")
        self.resizable(False, False)
        
        # Layout Griglia
        self.grid_columnconfigure(0, weight=1)

        # --- Componenti Grafici ---
        self.title_label = ctk.CTkLabel(
            self, 
            text="RUGBY ANALYTICS", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(50, 10))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Pulsantiera Allenatore di Bordo Campo", 
            font=ctk.CTkFont(size=13, text_color="gray")
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 40))

        self.username_input = ctk.CTkEntry(
            self, 
            placeholder_text="Username", 
            width=280, 
            height=40
        )
        self.username_input.grid(row=2, column=0, padx=20, pady=10)

        self.password_input = ctk.CTkEntry(
            self, 
            placeholder_text="Password", 
            show="*", 
            width=280, 
            height=40
        )
        self.password_input.grid(row=3, column=0, padx=20, pady=10)

        self.login_button = ctk.CTkButton(
            self, 
            text="Accedi", 
            command=self._on_login_click, 
            width=280, 
            height=42,
            font=ctk.CTkFont(weight="bold")
        )
        self.login_button.grid(row=4, column=0, padx=20, pady=(25, 15))

        self.status_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_label.grid(row=5, column=0, padx=20, pady=10)

    def _on_login_click(self):
        """Passa i dati al ViewModel all'evento di click."""
        username = self.username_input.get()
        password = self.password_input.get()
        
        self.login_button.configure(state="disabled")
        self.viewmodel.authenticate(username, password)

    def aggiorna_stato(self, messaggio: str, colore: str):
        """Metodo di callback invocato dal ViewModel per scrivere i log sulla GUI."""
        # Usiamo after(0) per sicurezza nel caso in cui la notifica arrivi dal thread di rete
        self.after(0, lambda: self.status_label.configure(text=messaggio, text_color=colore))
        if "Errore" in messaggio or "fallita" in messaggio or "Campi" in messaggio:
            self.after(0, lambda: self.login_button.configure(state="normal"))

    def gestisci_successo(self):
        """Invocato quando le credenziali sono verificate, avvisa l'app principale."""
        self.after(0, self.on_authenticated_callback)