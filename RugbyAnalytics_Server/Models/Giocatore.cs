using System;

namespace RugbyAnalytics.Server.Models
{
    //Classe astratta di rappresentazione dell'atleta
    public abstract class Giocatore
    {
        public int IdGiocatore { get; set; }
        public string Nome { get; set; } = string.Empty;
        public string Cognome { get; set; } = string.Empty;
        public int NumeroMaglia { get; set; }
        public string Reparto { get; set; } = string.Empty;

        public abstract double CalcolaIndiceEfficacia(int azioniPositive, int azioniTotali);
    }
}