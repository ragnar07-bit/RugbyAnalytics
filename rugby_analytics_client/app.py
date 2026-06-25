import customtkinter as ctk
from Network.socket_client import SocketClient
from viewmodels.login_viewmodel import LoginViewModel
from viewmodels.match_viewmodel import MatchViewModel
from views.login_window import LoginWindow
from views.match_window import MatchWindow

class RugbyAnalyticsApp:
    def __init__(self):
        # Impostiamo il tema grafico globale per tutte le finestre dell'applicazione
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue")

        # 1. Inizializzazione della logica di rete (Core)
        # Passiamo una funzione lambda come logger_callback per intercettare i log di rete 
        # e stamparli a terminale (o in futuro su un pannello di debug grafico)
        self.network_client = SocketClient(logger_callback=lambda msg: print(f"[APP-LOG] {msg}"))

        # 2. Inizializzazione dei ViewModel (Pattern MVVM)
        # Iniettiamo lo stesso client di rete in entrambi i ViewModel per condividere la connessione
        self.login_viewmodel = LoginViewModel(self.network_client)
        self.match_viewmodel = MatchViewModel(self.network_client)

        # 3. Riferimenti alle finestre dell'applicazione
        self.login_window = None
        self.match_window = None

    def run(self):
        """Avvia l'applicazione mostrando la finestra di login iniziale."""
        # Creiamo la finestra di login passandogli il suo ViewModel e la funzione da eseguire in caso di successo
        self.login_window = LoginWindow(
            viewmodel=self.login_viewmodel,
            on_authenticated_callback=self.switch_to_match_dashboard
        )
        # Avvia il loop principale dell'interfaccia grafica
        self.login_window.mainloop()

    def switch_to_match_dashboard(self):
        """Effettua il cambio di finestra chiudendo il login e aprendo la pulsantiera del match."""
        print("[APP] Autenticazione riuscita. Transizione alla Dashboard del Match...")
        
        # 1. Distruggiamo la finestra di login per liberare le risorse di sistema
        if self.login_window:
            self.login_window.destroy()

        # 2. Istanziamo e mostriamo la finestra principale del match (Dashboard)
        self.match_window = MatchWindow(viewmodel=self.match_viewmodel)
        
        # 3. Avviamo il loop grafico sulla nuova finestra principale
        self.match_window.mainloop()

if __name__ == "__main__":
    # Creazione dell'istanza del regista dell'applicazione e avvio
    app = RugbyAnalyticsApp()
    app.run()