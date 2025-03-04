using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Threading.Tasks;

public class TaxaSelicModel : PageModel
{
    private readonly TaxaSelicService _taxaSelicService;

    public string TaxaSelicData { get; private set; }

    public TaxaSelicModel(TaxaSelicService taxaSelicService)
    {
        _taxaSelicService = taxaSelicService;
    }

    public async Task OnGet()
    {
        
        TaxaSelicData = await _taxaSelicService.ObterTaxaSelic();
    }
}
