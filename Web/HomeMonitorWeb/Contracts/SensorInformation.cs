using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Contracts
{
    public class SensorInformation
    {
        public SensorInformation(int id, string location)
        {
            Id = id;
            Location = location;
        }
        public int Id { get; }

        public string Location { get; }
    }
}
