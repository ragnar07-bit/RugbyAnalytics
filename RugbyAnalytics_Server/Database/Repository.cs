using System;
using Microsoft.Data.Sqlite;
using RugbyAnalytics.Server.Models;

namespace RugbyAnalytics.Server.Database
{
    public class Repository
    {
        /// <summary>
        /// Recupera l'hash e il salt della password di un allenatore tramite lo username.
        /// (Materie coinvolte: Informatica per il DB, Sistemi per la Sicurezza)
        /// </summary>
        public static (string Hash, string Salt) GetCoachCredentials(string username)
        {
            using (var connection = DbConnector.GetConnection())
            {
                // Query parametrizzata standard per evitare SQL Injection (Fondamentale per la sicurezza)
                string query = "SELECT password_hash, password_salt FROM Allenatori WHERE username = @username LIMIT 1;";
                
                using (var command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@username", username);

                    using (var reader = command.ExecuteReader())
                    {
                        if (reader.Read())
                        {
                            string hash = reader.GetString(0);
                            string salt = reader.GetString(1);
                            return (hash, salt);
                        }
                    }
                }
            }
            return (string.Empty, string.Empty);
        }

        /// <summary>
        /// Salva in modo persistente un evento di gioco (KPI) inviato dal client a bordo campo.
        /// (Materia coinvolta: Informatica - Manipolazione dati SQL)
        /// </summary>
        public static bool SaveGameEvent(GameEventPacket packet)
        {
            try
            {
                using (var connection = DbConnector.GetConnection())
                {
                    string query = @"
                        INSERT INTO EventiMatch (id_giocatore, tipo_azione, timestamp) 
                        VALUES (@id_giocatore, @tipo_azione, @timestamp);";

                    using (var command = new SqliteCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("@id_giocatore", packet.IdGiocatore);
                        command.Parameters.AddWithValue("@tipo_azione", packet.TipoAzione);
                        command.Parameters.AddWithValue("@timestamp", packet.TimeStamp);

                        int rowsAffected = command.ExecuteNonQuery();
                        return rowsAffected > 0;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[ERRORE DB] Impossibile salvare l'evento match: {ex.Message}");
                return false;
            }
        }
    }
}