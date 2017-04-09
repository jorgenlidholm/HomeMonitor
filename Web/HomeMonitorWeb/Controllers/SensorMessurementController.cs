using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using HomeMonitorWeb.Contracts;
using HomeMonitorWeb.Validation;

namespace HomeMonitorWeb.Controllers
{
    [Produces("application/json")]
    [Route("api/[controller]")]
    public class SensorMessurementController : Controller
    {
        
        // GET: api/SensorMessurement/5
        [HttpGet("{id}")]
        public SensorMessurement Get(int id)
        {
            return new SensorMessurement(1, 23.0f, 33.0f);
        }
        
        // POST: api/SensorMessurement
        [HttpPost]
        public IActionResult Post([FromBody]SensorMessurement value)
        {
            if (!RequestValidation.Validate(Request.Headers))
                return Unauthorized();

            var measurement = value;

            return Ok();
        }
        
        // PUT: api/SensorMessurement/5
        [HttpPut("{id}")]
        public void Put(int id, [FromBody]string value)
        {
        }
        
        // DELETE: api/ApiWithActions/5
        [HttpDelete("{id}")]
        public void Delete(int id)
        {
        }
    }
}
