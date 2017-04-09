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
                new SensorInformation(21, "Tvättstuga"),
                new SensorInformation(135, "Matsal")
            };
        }

        // PUT api/SensorConfigurations/5
        [HttpGet("{id}")]
        public SensorInformation Get(int id)
        {
            return new SensorInformation(21, "Tvättstuga");
        }

        // PUT api/SensorConfigurations/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody]string value)
        {
        }
    }
}
