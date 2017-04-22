using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using HomeMonitorWeb.Contracts;
using HomeMonitorWeb.Validation;
using System.IO;
using System.Text;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using HomeMonitorWeb.Storage;

namespace HomeMonitorWeb.Controllers
{
    [Produces("application/json")]
    [Route("api/[controller]")]
    public class SensorMessurementController : Controller
    {
        private IOptions<SensorMessurementOptions> _configuration;
        private TableStorage _tableStorage;

        public SensorMessurementController(IOptions<SensorMessurementOptions> configuration, TableStorage tableStorage)
        {
            _configuration = configuration;
            _tableStorage = tableStorage;
        }

        // GET: api/SensorMessurement/5
        [HttpGet("{id}")]
        public IEnumerable<SensorMessurement> Get(int id)
        {
            return _tableStorage.Get(id).Result;
        }
        
        // POST: api/SensorMessurement
        [HttpPost]
        public IActionResult Post([FromBody]SensorMessurement value)
        {
                if (!RequestValidation.Validate(Request.Headers))
                return Unauthorized();
            try
            {
                var t1 = Task.Run(() => _tableStorage.Insert(value));

                t1.Wait();
            }
            catch (Exception ex)
            {
                return new StatusCodeResult(500);
            }
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
