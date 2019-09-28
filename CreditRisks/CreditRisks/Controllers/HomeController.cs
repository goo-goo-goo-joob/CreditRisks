using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Calcservice;
using Microsoft.AspNetCore.Mvc;
using CreditRisks.Models;
using Microsoft.AspNetCore.JsonPatch.Operations;
using PythonService;

namespace CreditRisks.Controllers
{
    public class HomeController : Controller
    {
        private readonly IPythonBackend _backend;

        public HomeController(IPythonBackend backend)
        {
            _backend = backend;
        }

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(Borrower model)
        {
            var r = _backend.Client.CalcProbability(new CalcRequest {INN = "asd"});
            model.DefaultProbability = r.Probability;
            return View(model);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel {RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier});
        }
    }
}