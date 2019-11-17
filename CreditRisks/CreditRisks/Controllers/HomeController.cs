using System.Diagnostics;
using Calcservice;
using CreditRisks.Models;
using Microsoft.AspNetCore.Mvc;
using PythonService;
using Dict = System.Collections.Generic.Dictionary<string, float>;

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


        private static Dict ObjectToDict(object obj)
        {
            var result = new Dict();
            return ObjectToDict(obj, result);
        }

        private static Dict ObjectToDict(object obj, Dict dict)
        {
            foreach (var prop in obj.GetType().GetProperties())
            {
                var propValue = prop.GetValue(obj, null);
                if (prop.PropertyType == typeof(float))
                    dict[prop.Name] = (float) propValue;
                else if (prop.PropertyType == typeof(int)) dict[prop.Name] = (int) propValue;
            }

            return dict;
        }

        [HttpPost]
        public IActionResult Index(Company model)
        {
            var borrower = new Borrower(model);
            var borrowerInfo = ObjectToDict(model);
            borrowerInfo = ObjectToDict(borrower, borrowerInfo);

            var request = new CalcRequest();
            request.Params.Add(borrowerInfo);
            request.INN = model.INN;
            var reply = _backend.Client.CalcProbability(request);
            model.DefaultProbability = borrower.CalcDefault().ToString("P2") + '_' + reply.Result;
            return View(model);
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel {RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier});
        }
    }
}