using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class SensorMessurementOptions
    {
        public SensorMessurementOptions()
        {
            StorageConnectionString = "String from ctor";
        }
        public string StorageConnectionString { get; set; }
    }
}
