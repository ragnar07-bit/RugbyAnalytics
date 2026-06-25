from Network.packet import Packet

class LoginViewModel:
    def __init__(self, network_client):
        self.network_client = network_client
        
        # Callback che verranno impostate dalla View per aggiornare la grafica
        self.on_status_changed = None
        self.on_login_success = None

    def authenticate(self, username, password):
        """Avvia la procedura di autenticazione tramite socket."""
        if not username or not password:
            self._notifica_stato("Compila tutti i campi!", "#FF3333")
            return

        self._notifica_stato("Connessione al server in corso...", "orange")

        # Tentativo di connessione TCP
        connesso = self.network_client.connect(
            on_packet_received_callback=self._handle_response,
            on_disconnect_callback=self._handle_disconnect
        )

        if connesso:
            self._notifica_stato("Verifica credenziali...", "#33FF33")
            # Preparazione del pacchetto di login
            login_payload = {"Username": username, "Password": password}
            packet = Packet("LOGIN", login_payload)
            self.network_client.send_packet(packet)
        else:
            self._notifica_stato("Errore: Server non raggiungibile", "#FF3333")

    def _handle_response(self, packet: Packet):
        """Gestisce la risposta JSON inviata dal server C#."""
        if packet.action == "LOGIN_RESPONSE":
            success = packet.data.get("Success", False)
            message = packet.data.get("Message", "")

            if success:
                self._notifica_stato("Accesso eseguito!", "#33FF33")
                if self.on_login_success:
                    self.on_login_success()
            else:
                self._notifica_stato(f"Errore: {message}", "#FF3333")
                self.network_client.disconnect()

    def _handle_disconnect(self):
        """Gestisce la perdita di connessione improvvisa."""
        self._notifica_stato("Connessione interrotta dal server", "#FF3333")

    def _notifica_stato(self, messaggio, colore):
        """Helper per inviare gli aggiornamenti di stato alla View se registrata."""
        if self.on_status_changed:
            self.on_status_changed(messaggio, colore)