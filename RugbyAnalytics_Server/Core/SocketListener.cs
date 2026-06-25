using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using RugbyAnalytics.Server.Database;
using RugbyAnalytics.Server.Models;
using RugbyAnalytics.Server.Security;

namespace RugbyAnalytics.Server.Core
{
    public class SocketListener
    {
        private readonly int _port;
        private TcpListener? _listener;
        private bool _isRunning;

        public SocketListener(int port = 5000)
        {
            _port = port;
        }

        /// <summary>
        /// Avvia il server TCP in ascolto sull'indirizzo IP locale (Any) e sulla porta specificata.
        /// (Materia: TPSIT - Socket asincroni e Programmazione concorrente)
        /// </summary>
        public async Task StartAsync()
        {
            _listener = new TcpListener(IPAddress.Any, _port);
            _listener.Start();
            _isRunning = true;
            Console.WriteLine($"[SERVER] In ascolto sulla porta {_port}...");

            try
            {
                while (_isRunning)
                {
                    // Accetta la connessione del client in modo non bloccante (Asincrono)
                    TcpClient client = await _listener.AcceptTcpClientAsync();
                    Console.WriteLine($"[SERVER] Nuovo client connesso: {client.Client.RemoteEndPoint}");

                    // Gestisce il client su un thread separato del ThreadPool (Multithreading concorrente)
                    _ = Task.Run(() => HandleClientAsync(client));
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[SERVER ERRORE] Errore nel ciclo di ascolto: {ex.Message}");
            }
        }

        /// <summary>
        /// Gestisce il ciclo di vita della comunicazione con un singolo client connesso.
        /// Implementa il protocollo applicativo di Framing (Header 4 byte + JSON Payload).
        /// </summary>
        private async Task HandleClientAsync(TcpClient client)
        {
            using (client)
            using (NetworkStream stream = client.GetStream())
            {
                byte[] headerBuffer = new byte[4];

                try
                {
                    while (_isRunning)
                    {
                        // 1. Legge l'Header di 4 byte (lunghezza in Big-Endian del payload JSON imminente)
                        int bytesRead = await stream.ReadAsync(headerBuffer, 0, 4);
                        if (bytesRead == 0) break; // Il client ha chiuso la connessione in modo pulito

                        // Converte i byte dell'header in un intero a 32 bit (Network Byte Order)
                        if (BitConverter.IsLittleEndian)
                        {
                            Array.Reverse(headerBuffer);
                        }
                        int payloadLength = BitConverter.ToInt32(headerBuffer, 0);

                        // 2. Legge l'esatto corpo del messaggio JSON in base alla lunghezza estratta dall'header
                        byte[] payloadBuffer = new byte[payloadLength];
                        int totalPayloadBytesRead = 0;

                        while (totalPayloadBytesRead < payloadLength)
                        {
                            int currentRead = await stream.ReadAsync(payloadBuffer, totalPayloadBytesRead, payloadLength - totalPayloadBytesRead);
                            if (currentRead == 0) throw new Exception("Connessione interrotta prematuramente dal client durante la ricezione del payload.");
                            totalPayloadBytesRead += currentRead;
                        }

                        // 3. Elabora il messaggio JSON grezzo
                        string jsonString = Encoding.UTF8.GetString(payloadBuffer);
                        Console.WriteLine($"[RETE] Ricevuto JSON: {jsonString}");

                        // Gestione dinamica dei messaggi basata sui campi del JSON (Routing del protocollo applicativo)
                        await ProcessMessageAsync(jsonString, stream);
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[RETE INFO] Client disconnesso ({client.Client.RemoteEndPoint}): {ex.Message}");
                }
            }
        }

        /// <summary>
        /// Deserializza e smista i pacchetti JSON in arrivo attivando la logica di business e DB.
        /// </summary>
        private async Task ProcessMessageAsync(string json, NetworkStream stream)
        {
            try
            {
                using (JsonDocument doc = JsonDocument.Parse(json))
                {
                    JsonElement root = doc.RootElement;

                    // Routing manuale basato sulla presenza di chiavi specifiche (Pattern Matching del protocollo)
                    if (root.TryGetProperty("Username", out _) && root.TryGetProperty("Password", out _))
                    {
                        // Gestione pacchetto LoginRequest
                        var loginReq = JsonSerializer.Deserialize<LoginRequest>(json);
                        if (loginReq != null)
                        {
                            Console.WriteLine($"[AUTENTICAZIONE] Richiesta di login per utente: {loginReq.Username}");
                            
                            // 1. Interroga lo strato Database (Informatica)
                            var (storedHash, storedSalt) = Repository.GetCoachCredentials(loginReq.Username);

                            bool isAuthenticated = false;
                            if (!string.IsNullOrEmpty(storedHash))
                            {
                                // 2. Verifica la sicurezza tramite Hashing SHA-256 + Salt (Sistemi)
                                isAuthenticated = CryptographyService.VerifyPassword(loginReq.Password, storedHash, storedSalt);
                            }

                            // 3. Prepara la risposta di rete (TPSIT)
                            var response = new LoginResponse
                            {
                                Success = isAuthenticated,
                                Message = isAuthenticated ? "Autenticazione riuscita!" : "Credenziali errate.",
                                SessionToken = isAuthenticated ? Guid.NewGuid().ToString() : string.Empty
                            };

                            await SendResponseAsync(response, stream);
                        }
                    }
                    else if (root.TryGetProperty("IdGiocatore", out _) && root.TryGetProperty("TipoAzione", out _))
                    {
                        // Gestione pacchetto GameEventPacket (KPI bordo campo)
                        var eventPacket = JsonSerializer.Deserialize<GameEventPacket>(json);
                        if (eventPacket != null)
                        {
                            Console.WriteLine($"[EVENTO MATCH] Ricevuta azione '{eventPacket.TipoAzione}' per giocatore ID: {eventPacket.IdGiocatore}");
                            
                            // Salva in modo persistente sul DB SQLite
                            bool isSaved = Repository.SaveGameEvent(eventPacket);
                            Console.WriteLine(isSaved ? "[DB] Evento match salvato correttamente." : "[DB ERRORE] Fallito salvataggio evento.");
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[PROTOCOLLO ERRORE] Errore nell'elaborazione del pacchetto: {ex.Message}");
            }
        }

        /// <summary>
        /// Invia una risposta strutturata al client applicando lo stesso principio di Framing (Header + Payload).
        /// </summary>
        private async Task SendResponseAsync(object responseObject, NetworkStream stream)
        {
            string jsonResponse = JsonSerializer.Serialize(responseObject);
            byte[] payloadBytes = Encoding.UTF8.GetBytes(jsonResponse);
            byte[] headerBytes = BitConverter.GetBytes(payloadBytes.Length);

            // Inversione per Network Byte Order (Big-Endian) se l'architettura locale è Little-Endian
            if (BitConverter.IsLittleEndian)
            {
                Array.Reverse(headerBytes);
            }

            // Invia prima i 4 byte dell'header e subito dopo il payload JSON
            await stream.WriteAsync(headerBytes, 0, 4);
            await stream.WriteAsync(payloadBytes, 0, payloadBytes.Length);
            await stream.FlushAsync();
        }

        /// <summary>
        /// Spegne il ciclo principale del server in modo sicuro.
        /// </summary>
        public void Stop()
        {
            _isRunning = false;
            _listener?.Stop();
            Console.WriteLine("[SERVER] Arrestato.");
        }
    }
}