using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace HomeMonitor.Library
{
    public class Authentication
    {
        readonly byte[] Secret = Encoding.UTF8.GetBytes("Äpplen, bananer och andra frukter");

        public bool ValidateAuthenticationToken(string key, string hashSecret)
        {
            using (var crypt = SHA256.Create())
            {
                var content = Secret.ToList();
                content.AddRange(Encoding.UTF8.GetBytes(key));
                var result = GetStringFromHash(crypt.ComputeHash(content.ToArray()));

                return String.Equals(result, hashSecret);
            }
        }

        public string GetAuthenticationToken(string key)
        {
            using (var crypt = SHA256.Create())
            {
                var content = Secret.ToList();
                content.AddRange(Encoding.UTF8.GetBytes(key));
                var result = GetStringFromHash(crypt.ComputeHash(content.ToArray()));
                return result;
            }
        }

        private static string GetStringFromHash(byte[] hash)
        {
            StringBuilder result = new StringBuilder();
            for (int i = 0; i < hash.Length; i++)
            {
                result.Append(hash[i].ToString("X2"));
            }
            return result.ToString().ToLower();
        }
    }
}
