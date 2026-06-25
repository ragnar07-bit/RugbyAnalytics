using System;
using System.IO;
using Microsoft.Data.Sqlite;

namespace RugbyAnalytics.Server.Database
{
    //Classe che rappresenta la connessione al DataBase relazionale
    public class DbConnector
    {
        private const string DbFileName = "rugby_analytics.db";
        private static readonly string ConnectionString = $"Data Source = {DbFileName}";

        //Restituisce una nuova istanza aperta di connessione al database SQLite
        public static SqliteConnection GetConnection()
        {
            //Definisco la variabile per aprire la connessione
            var connection = new SqliteConnection(ConnectionString);

            //Apro la connessione al database
            connection.Open();

            //Ritorno la connessione aperta
            return connection;
        }

        //Funzione che inizializza il database creando le tabelle 3NF se il file non esiste
        public static void InitializeDatabase()
        {
            if (File.Exists(DbFileName))
            {
                Console.WriteLine("[INFO] Database esistente rilevato!!!");
            }

            Console.WriteLine("[INFO] Inizializzazione nuovo database SQLite...");

            //Creazione delle tabelle
            using(var connection = GetConnection())
            {
                using(var command = connection.CreateCommand())
                {
                    // 1. Tabella Allenatori (Sistemi e Reti - Gestione Accessi)
                    command.CommandText = @"
                        CREATE TABLE IF NOT EXISTS Allenatori (
                            id_allenatore INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            password_hash TEXT NOT NULL,
                            password_salt TEXT NOT NULL
                        );";
                    command.ExecuteNonQuery();

                    // 2. Tabella Giocatori (Informatica - Corrispondenza con Classi OOP)
                    command.CommandText = @"
                        CREATE TABLE IF NOT EXISTS Giocatori (
                            id_giocatore INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            cognome TEXT NOT NULL,
                            numero_maglia INTEGER NOT NULL UNIQUE,
                            reparto TEXT NOT NULL CHECK(reparto IN ('Avanti', 'Trequarti'))
                        );";
                    command.ExecuteNonQuery();

                    // 3. Tabella EventiMatch (Informatica - Vincoli di Chiave Esterna e Integrità)
                    command.CommandText = @"
                        CREATE TABLE IF NOT EXISTS EventiMatch (
                            id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_giocatore INTEGER NOT NULL,
                            tipo_azione TEXT NOT NULL,
                            timestamp INTEGER NOT NULL,
                            FOREIGN KEY (id_giocatore) REFERENCES Giocatori(id_giocatore) ON DELETE CASCADE
                        );";
                    command.ExecuteNonQuery();

                    // Inserimento seed iniziale di un allenatore per i test a bordo campo
                    command.CommandText = @"
                        INSERT INTO Allenatori (username, password_hash, password_salt) 
                        VALUES ('admin', 'FintoHashDiTest67890=', 'FintoSalt12345=');";
                    command.ExecuteNonQuery();
                }
            }
            Console.WriteLine("[INFO] Database e tabelle relazionali create con successo!!");
        }
    }
}