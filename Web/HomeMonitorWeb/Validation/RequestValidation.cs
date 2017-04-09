using HomeMonitor.Library;
using Microsoft.AspNetCore.Http;

namespace HomeMonitorWeb.Validation
{
    public static class RequestValidation
    {
        public static bool Validate(IHeaderDictionary dict)
        {
            return ValidateRequest(dict.GetCommaSeparatedValues("X-HomeMonitor-Secret"));
        }
        private static bool ValidateRequest(string[] v)
        {
            if (v.Length != 2)
                return false;
            var auth = new Authentication();
            return auth.ValidateAuthenticationToken(v[0], v[1]);
        }
    }
}
