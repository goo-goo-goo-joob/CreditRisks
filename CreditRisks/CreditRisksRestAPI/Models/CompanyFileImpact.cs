using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Models
{
    public class CompanyFileImpact
    {
        [FromForm(Name = "file_report")] public IFormFile FileReport { get; set; }
        [FromForm(Name = "model_name")] public string ModelName { get; set; }
        [FromForm(Name = "feature")] public string Feature { get; set; }
        [FromForm(Name = "head")] public float Head { get; set; }
        [FromForm(Name = "tail")] public float Tail { get; set; }
    }
}