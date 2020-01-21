using System.Text;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Controllers
{
    [Route("")]
    [ApiController]
    public class IndexController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {

            return Content(Template.Render.RenderPage("Index.html", "base.html"), "text/html", Encoding.UTF8);
        }
    }

    [Route("CompanyFile")]
    [ApiController]
    public class FileController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {
            return Content(Template.Render.RenderPage("CompanyFile.html", "base.html"), "text/html", Encoding.UTF8);
        }
    }
}