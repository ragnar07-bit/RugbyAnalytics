using System;

namespace RugbyAnalytics.Server.Models
{
    //Classe che descrive il pacchetto inviato dal Client Python per richiedere l'autenticazione
    public class LoginRequest
    {
        public String Username { get; set; } = string.Empty;
        public String Password { get; set; } = string.Empty;
    }

    //Classe che descrive la risposta inviata dal Server C# dopo il controllo credenziali
    public class LoginResponse
    {
        public bool Success { get; set; }
        public string Message { get; set; } = string.Empty;
        public string SessionToken { get; set; } = string.Empty;
    }

    //Classe che descrive il pacchetto inviato dal Client in tempo reale ogni volta che viene premuto un tasto a bordo campo
    public class GameEventPacket
    {
        public int IdGiocatore { get; set; }
        public string TipoAzione { get; set; } = string.Empty;
        public long TimeStamp { get; set; }
    }
}