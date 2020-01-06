using System;
using System.Collections.Generic;
using System.IO;
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
            Company obj = new Company();
            Dictionary<string, string> dict = new Dictionary<string, string>();
            TextReader tr = new StreamReader(model.File.OpenReadStream());
            string line = tr.ReadLine();
            while (line != null)
            {
                var pair = line.Split('\t');
                dict[pair[0]] = pair[1];
                line = tr.ReadLine();
            }

            foreach (var prop in obj.GetType().GetProperties())
            {
                if (dict.TryGetValue(prop.Name, out var value))
                {
                    if (prop.PropertyType == typeof(string))
                        prop.SetValue(obj, value);
                    else if (prop.PropertyType == typeof(float))
                        prop.SetValue(obj, float.Parse(value));
                    else if (prop.PropertyType == typeof(int))
                        prop.SetValue(obj, int.Parse(value));
                    Console.WriteLine("{0} - {1}", prop.Name, value);
                }
            }

            return RedirectToAction("Index", "Home", new {model = obj});
        }
    }
}