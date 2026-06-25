from Network.packet import Packet

class MatchViewModel:
    def __init__(self, network_client):
        self.network_client = network_client
        
        # Stato locale del match per il tabellone
        self.punteggio_casa = 0
        self.punteggio_ospiti = 0
        
        # Callback impostata dalla MatchWindow per aggiornare la grafica
        self.on_match_data_changed = None

    def registra_evento_kpi(self, tipo_evento: str, giocatore_id: int, dettagli: dict = None):
        """Invia un evento KPI al backend C# tramite Socket."""
        if dettagli is None:
            dettagli = {}

        payload = {
            "EventType": tipo_evento,
            "PlayerId": giocatore_id,
            "Details": dettagli
        }
        
        packet = Packet("MATCH_KPI", payload)
        print(f"[MatchViewModel] Invio KPI: {tipo_evento} per il Giocatore ID {giocatore_id}")
        
        try:
            return self.network_client.send_packet(packet)
        except Exception as e:
            print(f"[MatchViewModel-ERROR] Impossibile inviare il pacchetto KPI: {e}")
            return False

    def aggiorna_punteggio(self, punti_casa: int, punti_ospiti: int):
        """Aggiorna lo stato del punteggio locale e notifica la finestra grafica."""
        self.punteggio_casa += punti_casa
        self.punteggio_ospiti += punti_ospiti
        
        if self.on_match_data_changed:
            self.on_match_data_changed()