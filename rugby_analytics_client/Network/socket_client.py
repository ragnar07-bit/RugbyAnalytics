import socket
import threading
from Network.packet import Packet

class SocketClient:
    #Costruttore di default
    def __init__(self, host="127.0.0.1", port=5000, logger_callback=None):
        self.host = host
        self.port = port
        self.client_socket = None
        self.is_connected = False
        self.listen_thread = None
        # Gestore di log personalizzato (se assente, usa il print predefinito)
        self.log = logger_callback if logger_callback is not None else print
    
    #Metodo che stabilisce la connessione TCP asincrona con il server
    def connect(self, on_packet_received_callback, on_disconnect_callback):
        try:
            #Creazione e connessione del socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            self.log(f"[NETWORK] Connesso con successo al server {self.host}:{self.port}")

            #Avvia l'ascolto in background per non congelare la View
            self.listen_thread = threading.Thread(
                target=self._listen_to_server,
                args=(on_packet_received_callback, on_disconnect_callback),
                daemon=True
            )
            self.listen_thread.start()

            return True
        except Exception as e:
            self.log(f"[NETWORK ERROR] Impossibile stabilire la connesione: {e}")
            self.is_connected = False
            
            return False
    
    #Metodo per l'invio di un oggetto Packet serializzato in formato JSON
    def send_packet(self, packet: Packet) -> bool:
        if not self.is_connected or not self.client_socket:
            self.log("[NETWORK ERROR] Invio fallito: Socket non connesso!!")

            return False
        
        #Serializzazione del pacchetto
        try:
            raw = packet.to_json_string()
            self.client_socket.sendall(raw.encode('utf-8'))
            self.log(f"[NETWORK SEND] Inviato pacchetto con Action: '{packet.action}'")
            
            return True
        except Exception as e:
            self.log(f"[NETWORK ERROR] Errore durante la trasmissione: {e}")
            
            return False
    
    #Metodo che gestisce il cliclo di lettura continuo eseguito in background
    def _listen_to_server(self, on_packet_received_callback, on_disconnect_callback):
        buffer = ""

        while self.is_connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    self.log("[NETWORK] Connessione interrotta dal server remoto.")
                    break

                buffer += data.decode('utf-8')

                #Elabora i pacchetti separati dal terminatore di riga \n
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)

                    if line.strip():
                        #Trasformo la riga JSON grezza in un oggetto Packet
                        received_packet = Packet.from_json_string(line)
                        
                        if received_packet:
                            self.log(f"[NETWORK IN] Ricevuto pacchetto con Action: '{received_packet.action}'")
                            #Passo l'oggetto Packet alla GUI o all'app principale
                            on_packet_received_callback(received_packet)
            except Exception as e:
                self.log(f"[NETWORK ERROR] Connessione chiussa inaspettatamente: {e}")
                break
        
        #Routine di chiusura pulita delle risorse
        self.is_connected = False

        if self.client_socket:
            self.client_socket.close()
        on_disconnect_callback()
    
    #Metodo di chiusura della sessione corrente del socket
    def disconnect(self):
        self.is_connected = False

        if self.client_socket:
            self.client_socket.close()
        self.log("[NETWORK] Socket chiuso dall'applicazione client!")