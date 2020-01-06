using CreditRisks.Models;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisks.Controllers
{
    public class CompanyFileController : Controller
    {
        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(CompanyFile model)
        {
            return View(model);
        }
    }
}