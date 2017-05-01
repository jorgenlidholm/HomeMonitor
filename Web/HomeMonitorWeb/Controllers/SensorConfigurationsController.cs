using HomeMonitorWeb.Contracts;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace HomeMonitorWeb.Controllers
{
    [Produces("application/json")]
    [Route("api/[controller]")]
    public class SensorConfigurationsController : Controller
    {
        public SensorConfigurationsController()
        {

        }
        // PUT api/SensorConfigurations
        [HttpGet]
        public IEnumerable<SensorInformation> GetAll()
        {
            return new List<SensorInformation>
            {
                new SensorInformation(21,21,"Tvättstuga"),
                new SensorInformation(135, 135, "Matsal"),
                new SensorInformation(1, 11, "Golvvärmecentral"),
                new SensorInformation(3, 31, "Källare trapphus"),
                new SensorInformation(4, 41, "Vind, ovan TV rum"),
            };
        }

        // PUT api/SensorConfigurations/5
        [HttpGet("{id}")]
        public SensorInformation Get(int id)
        {
            return new SensorInformation(21,21, "Tvättstuga");
        }

        // PUT api/SensorConfigurations/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody]string value)
        {
        }
    }
}
