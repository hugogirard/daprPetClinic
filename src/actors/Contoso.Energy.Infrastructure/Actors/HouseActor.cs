using Contoso.Energy.Infrastructure.Models;
using Dapr.Actors.Runtime;
using Microsoft.Extensions.Logging;
namespace Contoso.Energy.Infrastructure.Actors;

public class HouseActor : Actor, IHouseActor
{
    private const string CurrentTemperatureKey = "currentTemperature";
    private const string TargetTemperatureKey = "targetTemperature";
    private const double DefaultTemperature = 20.0;
    private const double TemperatureTolerance = 0.5;

    public HouseActor(ActorHost host) : base(host)
    {
    }

    protected override async Task OnActivateAsync()
    {
        // Initialize default temperatures if not set
        var currentTemp = await StateManager.TryGetStateAsync<double>(CurrentTemperatureKey);
        if (!currentTemp.HasValue)
        {
            await StateManager.SetStateAsync(CurrentTemperatureKey, DefaultTemperature);
        }

        var targetTemp = await StateManager.TryGetStateAsync<double>(TargetTemperatureKey);
        if (!targetTemp.HasValue)
        {
            await StateManager.SetStateAsync(TargetTemperatureKey, DefaultTemperature);
        }

        await StateManager.SaveStateAsync();
    }

    public async Task SetTemperatureAsync(double temperature)
    {
        await StateManager.SetStateAsync(CurrentTemperatureKey, temperature);
        await StateManager.SaveStateAsync();

        Logger.LogInformation("House {HouseId}: Current temperature set to {Temperature}°C",
            Id.GetId(), temperature);
    }

    public async Task<double> GetTemperatureAsync()
    {
        return await StateManager.GetStateAsync<double>(CurrentTemperatureKey);
    }

    public async Task SetTargetTemperatureAsync(double targetTemperature)
    {
        await StateManager.SetStateAsync(TargetTemperatureKey, targetTemperature);
        await StateManager.SaveStateAsync();

        Logger.LogInformation("House {HouseId}: Target temperature set to {Temperature}°C",
            Id.GetId(), targetTemperature);
    }

    public async Task<double> GetTargetTemperatureAsync()
    {
        return await StateManager.GetStateAsync<double>(TargetTemperatureKey);
    }

    public async Task<ThermostatStatus> GetThermostatStatusAsync()
    {
        var currentTemp = await GetTemperatureAsync();
        var targetTemp = await GetTargetTemperatureAsync();

        var isHeating = currentTemp < targetTemp - TemperatureTolerance;
        var isCooling = currentTemp > targetTemp + TemperatureTolerance;

        return new ThermostatStatus(
            currentTemp,
            targetTemp,
            isHeating,
            isCooling,
            DateTime.UtcNow
        );
    }
}
