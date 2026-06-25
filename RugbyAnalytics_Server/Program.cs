using System;
using System.Threading.Tasks;
using RugbyAnalytics.Server.Database;
using RugbyAnalytics.Server.Core;

namespace RugbyAnalytics.Server
{
    class Program
    {
        //Entry point principale del Server
        static async Task Main(string[] args)
        {
            Console.Title = "RugbyAbalytics Server - Dashboard di Controllo";

            Console.WriteLine("=======================================================");
            Console.WriteLine("   RUGBY ANALYTICS ENTERPRISE - SERVER SUB-SYSTEM      ");
            Console.WriteLine("=======================================================");
            Console.WriteLine($"[AVVIO] Ora locale: {DateTime.Now}");
            Console.WriteLine("[AVVIO] Sistema Operativo: Fedora Linux");
            Console.WriteLine("-------------------------------------------------------");

            try
            {
                //1.Inizializzazione dello strato di persistenza
                DbConnector.InitializeDatabase();

                //2.Istanzazione e avvio dello strato di rete
                int portaServer = 5000;
                SocketListener server = new SocketListener(portaServer);

                //Avvio del server in un Task asincrono separato
                Task serverTask = server.StartAsync();

                Console.WriteLine("-------------------------------------------------------");
                Console.WriteLine("[INFO] Server inizializzato correttamente ed è operativo.");
                Console.WriteLine("[INFO] Premi [INVIO] in qualsiasi momento per arrestare il server.");
                Console.WriteLine("=======================================================");

                //Mantiene attiva l'applicazione console in attesa dell'input dell'utente
                Console.ReadLine();

                //3.Spegnimento controllato e rilascio delle risorse
                Console.WriteLine("[LOG] Ricevuto comando di arresto. Spegnimento in corso...");
                server.Stop();

                //Attende che il task del server si chiuda definitivamente
                await serverTask;
            }
            catch(Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"[CRITICAL ERROR] Errore fatale all'avvio del server: {ex.Message}");
                Console.ResetColor();
            }

            Console.WriteLine("[LOG] Server spento correttamente! Arrivederci");
        }
    }
}