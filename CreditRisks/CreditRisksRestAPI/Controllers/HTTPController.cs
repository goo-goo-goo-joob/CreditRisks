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
            return Content(Template.Render.RenderPage("CompanyFile.html", "base.html"), "text/html", Encoding.UTF8);
        }
    }

    [Route("static/")]
    [ApiController]
    public class StaticController : ControllerBase
    {
        [HttpGet("site.js")]
        public ActionResult<string> GetJs()
        {
            return Content(Template.Render.RenderPage("site.js"), "application/javascript", Encoding.UTF8);
        }

        [HttpGet("site.css")]
        public ActionResult<string> GetCss()
        {
            return Content(Template.Render.RenderPage("site.css"), "text/css", Encoding.UTF8);
        }
    }
}