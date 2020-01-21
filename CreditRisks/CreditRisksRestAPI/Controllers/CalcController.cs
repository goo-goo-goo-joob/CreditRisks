using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using CreditRisksRestAPI.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CalculateController : ControllerBase
    {
        // GET api/values
        [HttpGet]
        public ActionResult<IEnumerable<string>> Get()
        {
            return new string[] {"value1", "value2"};
        }

        // POST api/values
        [HttpPost]
        public void Post([FromForm] CompanyFileMain value)
        {
            Console.WriteLine(value);
        }
    }
}