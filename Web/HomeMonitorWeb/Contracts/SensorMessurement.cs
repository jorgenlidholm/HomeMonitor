using Microsoft.WindowsAzure.Storage.Table;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class SensorMessurement
    {
        public SensorMessurement(int identity, long time, float temperature, float humidity)
        {
            Time = time;
            Identity = identity;
            Temperature = temperature;
            Humidity = humidity;
        }
        public int Identity { get; }
        public float Temperature { get; }
        public float Humidity { get; }
        public long Time { get; }
    }

    public class SensorMessurementArray
    {
        public SensorMessurement[] messurments { get; set; }
    }

    public class SensorMessurementEntity : TableEntity
    {
        public SensorMessurementEntity(int identity, long time)
        {
            PartitionKey = identity.ToString();
            RowKey = time.ToString();
            Identity = identity;
            Time = time;
        }
        public SensorMessurementEntity()
        {
        }

        public int Identity { get; set; }
        public long Time { get; set; }
        public double Temperature { get; set; }
        public double Humidity { get; set; }
    }
}
