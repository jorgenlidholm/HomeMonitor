using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class LightingConfiguration
    {
        public LightingConfiguration(bool lightOnSundown, bool lightOfAtNight)
        {
            LightOnSundown = lightOnSundown;
            LightOffAtNight = lightOfAtNight;
        }


        public bool LightOnSundown { get; }

        public bool LightOffAtNight { get; set; }
    }
}
