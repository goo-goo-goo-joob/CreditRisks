using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Controllers
{
    [Route("")]
    [ApiController]
    public class HttpController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {
            return "value";
        }
    }
}