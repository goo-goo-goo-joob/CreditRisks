using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Calcservice;
using CreditRisksRestAPI.Models;
using Google.Protobuf;
using Google.Protobuf.Collections;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using PythonService;
using Borrower = CreditRisksRestAPI.Models.Borrower;
using Company = CreditRisksRestAPI.Models.Company;
using Dict = System.Collections.Generic.Dictionary<string, string>;

namespace CreditRisksRestAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CalculateController : ControllerBase
    {
        private readonly IPythonBackend _backend;

        public CalculateController(IPythonBackend backend)
        {
            _backend = backend;
        }

        // GET api/values
        [HttpGet]
        public ActionResult<IEnumerable<string>> Get()
        {
            return new string[] {"value1", "value2"};
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
                if (propValue != null)
                {
                    dict[prop.Name] = propValue.ToString();
                }
            }

            return dict;
        }

        // POST api/values
        [HttpPost]
        public ActionResult<string> Post([FromForm] CompanyFileMain model)
        {
            Company obj = new Company();
            Dictionary<string, string> dictCSharp = new Dictionary<string, string>();
            Dictionary<string, string> dictPython = new Dictionary<string, string>();
            TextReader tr = new StreamReader(model.FileReport.OpenReadStream());
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
            var dictionary = new Dictionary<string, string> {["Модель из методики"] = borrower.CalcDefault().ToString("P2")};
            foreach (KeyValuePair<string, float> pair in reply.Result)
            {
                dictionary[pair.Key] = pair.Value.ToString("P2");
            }

            return Content(JsonConvert.SerializeObject(dictionary), "application/json", Encoding.UTF8);
        }
    }

    [Route("api/[controller]")]
    [ApiController]
    public class ModelController : ControllerBase
    {
        private readonly IPythonBackend _backend;

        public ModelController(IPythonBackend backend)
        {
            _backend = backend;
        }

        [HttpGet("{name}")]
        public ActionResult<string> Get(string name)
        {
            var request = new ModelInfoRequest {ModelName = name};
            var reply = _backend.Client.GetModelInfo(request);
            var result = new Dictionary<string, string>();
            foreach (KeyValuePair<string, ByteString> pair in reply.Result)
            {
                result[pair.Key] = pair.Value.ToBase64();
            }

            return Content(JsonConvert.SerializeObject(result), "application/json", Encoding.UTF8);
        }
    }
}