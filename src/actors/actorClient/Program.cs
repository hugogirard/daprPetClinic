using Contoso.Energy.Infrastructure.Actors;
using Dapr.Actors;
using Dapr.Actors.Client;

Console.WriteLine("Starting Up");

List<ActorId> houses = new List<ActorId>
{
    new ActorId("hugoHouse"),
    new ActorId("johnHouse"),
    new ActorId("jessHouse")
};

var actorType = "HouseActor";

var actorProxyOptions = new ActorProxyOptions
{
    HttpEndpoint = "http://localhost:3500"
};

List<IHouseActor> actors = new List<IHouseActor>();

foreach (var house in houses) 
{
    actors.Add(ActorProxy.Create<IHouseActor>(house, actorType));
}

// Set initial target temperatures for each house
await actors[0].SetTargetTemperatureAsync(22.0); // Hugo's house
await actors[1].SetTargetTemperatureAsync(20.0); // John's house
await actors[2].SetTargetTemperatureAsync(24.0); // Jess's house

// Set initial current temperatures
await actors[0].SetTemperatureAsync(18.0);
await actors[1].SetTemperatureAsync(19.0);
await actors[2].SetTemperatureAsync(21.0);

Console.WriteLine("Initial temperatures set. Starting monitoring...\n");

var random = new Random();
int iteration = 0;

while (true)
{
    iteration++;
    Console.WriteLine($"=== Iteration {iteration} - {DateTime.Now:HH:mm:ss} ===");

    // Update temperature every 5 seconds
    if (iteration % 5 == 0)
    {
        // Simulate temperature changes with random fluctuations
        await actors[0].SetTemperatureAsync(18.0 + random.NextDouble() * 8.0); // 18-26°C
        await actors[1].SetTemperatureAsync(19.0 + random.NextDouble() * 6.0); // 19-25°C
        await actors[2].SetTemperatureAsync(21.0 + random.NextDouble() * 7.0); // 21-28°C

        Console.WriteLine("📡 Temperature updates sent to all houses");
    }

    // Display current status for all houses
    for (int i = 0; i < actors.Count; i++)
    {
        var status = await actors[i].GetThermostatStatusAsync();
        var houseName = houses[i].GetId();

        var heatingIcon = status.IsHeating ? "🔥" : "  ";
        var coolingIcon = status.IsCooling ? "❄️ " : "  ";

        Console.WriteLine($"{heatingIcon}{coolingIcon} {houseName,-15} | Current: {status.CurrentTemperature:F1}°C | Target: {status.TargetTemperature:F1}°C");
    }

    Console.WriteLine();

    // Sleep for 1 second
    await Task.Delay(3000);
}