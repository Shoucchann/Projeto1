public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddHttpClient<TaxaSelicService>(); 
        services.AddRazorPages();
    }
}
