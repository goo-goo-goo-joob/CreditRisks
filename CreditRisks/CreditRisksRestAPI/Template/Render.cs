using System.IO;

namespace CreditRisksRestAPI.Template
{
    public class Render
    {
        private const string Label = "###CONTENT###";
        private const string Path = "Template/";

        public static string RenderPage(string filename, string source)
        {
            string sourceText = File.ReadAllText(Path + source);
            string doc = File.ReadAllText(Path + filename);
            return sourceText.Replace(Render.Label, doc);
        }

        public static string RenderPage(string filename)
        {
            return File.ReadAllText(Path + filename);
        }
    }
}