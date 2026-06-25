using System;
using System.Runtime.Intrinsics.Arm;
using System.Security.Cryptography;
using System.Text;

namespace RugbyAnalytics.Server.Security
{
    public class CryptographyService
    {
        //Genera un Salt crittograficamente sicuro composto da byte casuali convertiti in Base64.
        public static string GenerateSalt(int size = 16)
        {
            byte[] buffer = new byte[size];

            using (var rng = RandomNumberGenerator.Create())
            {
                //Riempio il buffer con byte casuali forti generati dal sistema operativo
                rng.GetBytes(buffer);
            }

            return Convert.ToBase64String(buffer);
        }

        //Calcola l'hash SHA-256 della password unita al salt
        public static string ComputeHash(string password, string salt)
        {
            string combinedInput = password + salt;

            using(SHA256 sha256 = SHA256.Create())
            {
                byte[] inputBytes = Encoding.UTF8.GetBytes(combinedInput);
                byte[] hashBytes = sha256.ComputeHash(inputBytes);

                return Convert.ToBase64String(hashBytes);
            }
        }

        //Funzione che verifica la password in input confrontando gli hash a tempo costante per mitigare i Timing Attacks.
        public static bool VerifyPassword(string inputPassword, string storeHash, string sotredSalt)
        {
            string computeHash = ComputeHash(inputPassword, sotredSalt);

            byte[] computedBytes = Convert.FromBase64String(computeHash);
            byte[] storedBytes = Convert.FromBase64String(storeHash);

            // Se le lunghezze differiscono, le password non corrispondono
            if (computedBytes.Length != storedBytes.Length)
            {
                return false;
            }

            // Confronto a tempo fisso (O(1)) tramite operatore XOR.
            // Previene i Timing Attacks impedendo a un attaccante di indovinare l'hash 
            // misurando i cicli di clock della CPU della macchina server.
            int result = 0;
            for (int i = 0; i < computedBytes.Length; i++)
            {
                result |= computedBytes[i] ^ storedBytes[i];
            }

            return result == 0;
        }
    }
}