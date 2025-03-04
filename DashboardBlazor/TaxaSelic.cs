using System.Net.Http;
using System.Threading.Tasks;

public class TaxaSelicService
{
    private readonly HttpClient _httpClient;

    public TaxaSelicService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<string> ObterTaxaSelic()
    {
        // URL da API Python
        string url = "http://127.0.0.1:8000/taxaSelic";
        var response = await _httpClient.GetStringAsync(url);
        return response;
    }
}
