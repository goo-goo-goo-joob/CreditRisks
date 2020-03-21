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

        public CalculateController()
        {
            _backend = new PythonBackend();
        }

        [HttpPost]
        public ActionResult<string> Post([FromForm] CompanyFileMain model)
        {
            Company obj = new Company();
            Dictionary<string, string> dictCSharp = new Dictionary<string, string>();
            Dictionary<string, string> dictPython = new Dictionary<string, string>();
            // TextReader tr = new StreamReader(model.FileReport.OpenReadStream());
            Dictionary<string, string> values = JsonConvert.DeserializeObject<Dictionary<string, string>>(model.Data);
            // string line = tr.ReadLine();
            foreach (KeyValuePair<string,string> pair in values)
            {
                // var pair = line.Split('\t');
                string name = pair.Key;
                string value = pair.Value;
                dictPython[name] = value;
                if (name.StartsWith("year_0_"))
                {
                    // Данные отчтетности за текущий год
                    var parts = name.Split('_');
                    dictCSharp[String.Join('_', "Code", parts[2])] = value;
                }
                else if (name.StartsWith("year_-1_") || Array.IndexOf(new[] {"year_-1", "year_0", "region"}, name) >= 0)
                {
                    // Данные отчетности за предыдущий год
                }
                else
                {
                    // Другие данные, например нефинансовые показатели
                    dictCSharp[name] = value;
                }

                
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
            // request.INN = model.Inn ?? "";
            var reply = _backend.Client.CalcProbability(request);
            var dictionary = new Dictionary<string, string>();
            foreach (KeyValuePair<string, float> pair in reply.Result)
            {
                dictionary[pair.Key] = pair.Value.ToString("P2");
            }

//            dictionary["Регрессия банка"] = borrower.CalcDefault().ToString("P2");
            return Content(JsonConvert.SerializeObject(dictionary), "application/json", Encoding.UTF8);
        }
    }

    [Route("api/[controller]")]
    [ApiController]
    public class ModelController : ControllerBase
    {
        private readonly IPythonBackend _backend;

        public ModelController()
        {
            _backend = new PythonBackend();
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

    [Route("api/[controller]")]
    [ApiController]
    public class ImpactController : ControllerBase
    {
        private readonly IPythonBackend _backend;

        public ImpactController()
        {
            _backend = new PythonBackend();
        }

        [HttpPost]
        public ActionResult<string> Post([FromForm] CompanyFileImpact model)
        {
            Dictionary<string, string> dictPython = new Dictionary<string, string>();
            TextReader tr = new StreamReader(model.FileReport.OpenReadStream());
            string line = tr.ReadLine();
            while (line != null)
            {
                var pair = line.Split('\t');
                string name = pair[0];
                string value = pair[1];

                dictPython[name] = value;

                line = tr.ReadLine();
            }


            var request = new ImpactRequest {ModelName = model.ModelName, Feature = model.Feature, Head = model.Head, Tail = model.Tail};
            request.Data.Add(dictPython);

            var reply = _backend.Client.GetImpact(request);
            return Content(JsonConvert.SerializeObject(reply.Image.ToBase64()), "application/json", Encoding.UTF8);
        }
    }
}