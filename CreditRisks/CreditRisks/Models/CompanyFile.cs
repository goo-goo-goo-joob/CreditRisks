using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Http;

namespace CreditRisks.Models
{
    public class CompanyFile
    {
        [StringLength(10, MinimumLength = 10)]
        public string INN { get; set; }
        public IFormFile File { set; get; }
    }
}