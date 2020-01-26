using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace CreditRisksRestAPI.Models
{
    public class CompanyFileMain
    {
        [FromForm(Name = "inn")] public string Inn { get; set; }
        [FromForm(Name = "file_report")] public IFormFile FileReport { get; set; }
    }
}