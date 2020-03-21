using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Models
{
    public class CompanyFileMain
    {
        [FromForm(Name = "data")] public string Data { get; set; }
        // [FromForm(Name = "file_report")] public IFormFile FileReport { get; set; }
    }
}