from Network.packet import Packet

class MatchViewModel:
    def __init__(self, network_client):
        self.network_client = network_client
        
        # Stato locale del match (Reattivo per la futura Dashboard)
        self.punteggio_casa = 0
        self.punteggio_ospiti = 0
        self.cronometro = "00:00"
        
        # Callback per aggiornare la DashboardView quando cambiano i dati
        self.on_match_data_changed = None

    def registra_evento_kpi(self, tipo_evento: str, giocatore_id: int, dettagli: dict = None):
        """
        Invia un evento KPI (es. 'META', 'PLACCAGGIO', 'TOUCHE') al server C#.
        """
        if dettagli is None:
            dettagli = {}

        payload = {
            "EventType": tipo_evento,
            "PlayerId": giocatore_id,
            "Details": dettagli
        }
        
        # Creiamo il pacchetto standardizzato per i KPI del match
        packet = Packet("MATCH_KPI", payload)
        
        # Invio asincrono su Socket
        successo = self.network_client.send_packet(packet)
        return successo

    def aggiorna_punteggio(self, punti_casa: int, punti_ospiti: int):
        """Aggiorna lo stato locale e notifica la View."""
        self.punteggio_casa += punti_casa
        self.punteggio_ospiti += punti_ospiti
        
        if self.on_match_data_changed:
            self.on_match_data_changed()