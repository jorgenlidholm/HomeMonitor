using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using HomeMonitor.Library;
using HomeMonitorWeb.Contracts;
using HomeMonitorWeb.Validation;

namespace HomeMonitorWeb.Controllers
{
    [Produces("application/json")]
    [Route("api/[controller]")]
    public class LightingConfigurationsController : Controller
    {
        // GET: api/LightingConfiguration
        [HttpGet]
        public LightingConfiguration Get()
        {
            if (!RequestValidation.Validate(Request.Headers))
                throw new UnauthorizedAccessException();


            return new LightingConfiguration(true, true);
        }



        // GET: api/LightingConfiguration/5
        [HttpGet("{id}")]
        public LightingConfiguration Get(int id)
        {

            return new LightingConfiguration(true, true);
        }
        
        // POST: api/LightingConfiguration
        [HttpPost]
        public void Post([FromBody]string value)
        {
        }
        
        // PUT: api/LightingConfiguration/5
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
