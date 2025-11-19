using Contoso.Energy.Infrastructure.Actors;
using Microsoft.Extensions.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddActors(options => 
{
    options.Actors.RegisterActor<HouseActor>();
});

//builder.Services.AddDaprSidekick(builder.Configuration, options =>
//{
//    //options.Sidecar = new Man.Dapr.Sidekick.DaprSidecarOptions
//    //{
//    //    AppId = "house-actor",
//    //    DaprHttpPort = 3515
//    //};
//});

var app = builder.Build();

app.UseDeveloperExceptionPage();

app.UseHttpsRedirection();

// Register actors handlers that interface with the Dapr runtime.
app.MapActorsHandlers();

app.Run();


