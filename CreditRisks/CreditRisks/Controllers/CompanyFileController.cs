using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Calcservice;
using CreditRisks.Models;
using Microsoft.AspNetCore.Mvc;
using PythonService;

namespace CreditRisks.Controllers
{
    public class CompanyFileController : Controller
    {
        private readonly IPythonBackend _backend;

        public CompanyFileController(IPythonBackend backend)
        {
            _backend = backend;
        }

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(CompanyFile model)
        {
            Company obj = new Company();
            Dictionary<string, string> dictCSharp = new Dictionary<string, string>();
            Dictionary<string, string> dictPython = new Dictionary<string, string>();
            TextReader tr = new StreamReader(model.File.OpenReadStream());
            string line = tr.ReadLine();
            while (line != null)
            {
                var pair = line.Split('\t');
                string name = pair[0];
                string value = pair[1];

                if (name.StartsWith("year_0_"))
                {
                    // Данные отчтетности за текущий год
                    var parts = name.Split('_');
                    dictCSharp[String.Join('_', "Code", parts[2])] = value;
                    dictPython[name] = value;
                }
                else if (name.StartsWith("year_-1_") || Array.IndexOf(new[] {"year_-1", "year_0", "region"}, name) >= 0)
                {
                    // Данные отчетности за предыдущий год
                    dictPython[name] = value;
                }
                else
                {
                    // Другие данные, например нефинансовые показатели
                    dictCSharp[name] = value;
                }

                line = tr.ReadLine();
            }

            foreach (var prop in obj.GetType().GetProperties())
            {
                if (dictCSharp.TryGetValue(prop.Name, out var value))
                {
                    if (prop.PropertyType == typeof(float))
                        prop.SetValue(obj, float.Parse(value));
                    else if (prop.PropertyType == typeof(int))
                        prop.SetValue(obj, int.Parse(value));
                }
            }

            var borrower = new Borrower(obj);

            var request = new CalcRequest();
            request.Params.Add(dictPython);
            request.INN = model.Inn ?? "";
            var reply = _backend.Client.CalcProbability(request);
            model.DefaultProbability = new Dictionary<string, string> {["Модель из методики"] = borrower.CalcDefault().ToString("P2")};
            foreach (KeyValuePair<string, float> pair in reply.Result)
            {
                model.DefaultProbability[pair.Key] = pair.Value.ToString("P2");
            }

            return View(model);
        }
    }
}