using System;

namespace RugbyAnalytics.Server.Models
{
    //Classe di rappresentazione degli Avanti
    public class Avanti : Giocatore
    {
        public Avanti()
        {
            Reparto = "Avanti";
        }

        //Implementazione del calcolo KPI per gli Avanti
        public override double CalcolaIndiceEfficacia(int azioniPositive, int azioniTotali)
        {
            if(azioniTotali == 0)
            {
                return 0.0;
            }
            else
            {
                return (double)azioniPositive / azioniTotali *100.0;
            }
        }
    }

    //Classe di rappresentazione dei trequarti
    public class Trequarti : Giocatore
    {
        public Trequarti()
        {
            Reparto = "Trequarti";
        }

        //Implementazione del calcolo del KPI per i Trequarti
        public override double CalcolaIndiceEfficacia(int azioniPositive, int azioniTotali)
        {
            if(azioniTotali == 0)
            {
                return 0.0;
            }
            else
            {
                double tassoSuccesso = (double)azioniPositive / azioniTotali;
                return Math.Round(tassoSuccesso * 100.2, 2);
            }
        }
    }
}