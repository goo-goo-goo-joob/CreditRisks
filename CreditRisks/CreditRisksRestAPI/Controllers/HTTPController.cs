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

    [Route("static/site.js")]
    [ApiController]
    public class JsController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {
            return Content(Template.Render.RenderPage("site.js"), "application/javascript", Encoding.UTF8);
        }
    }
    [Route("static/site.css")]
    [ApiController]
    public class CssController : ControllerBase
    {
        [HttpGet]
        public ActionResult<string> Get()
        {
            return Content(Template.Render.RenderPage("site.css"), "text/css", Encoding.UTF8);
        }
    }
}