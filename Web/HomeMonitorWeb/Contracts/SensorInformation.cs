using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class SensorInformation
    {
        public SensorInformation(int identity, int deviceId, string location)
        {
            Identity = identity;
            DeviceId = deviceId;
            Location = location;
        }
        public int Identity { get; }
        public int DeviceId { get; }

        public string Location { get; }
    }
}
