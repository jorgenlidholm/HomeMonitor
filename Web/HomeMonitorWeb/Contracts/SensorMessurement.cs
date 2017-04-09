using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class SensorMessurement
    {
        public SensorMessurement(int identity, float temperature, float humidity)
        {
            Identity = identity;
            Temperature = temperature;
            Humidity = humidity;
        }
        public int Identity { get; }
        public float Temperature { get; }
        public float Humidity { get; }
    }
}
