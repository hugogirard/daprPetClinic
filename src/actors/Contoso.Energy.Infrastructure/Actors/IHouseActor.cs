using Contoso.Energy.Infrastructure.Models;
using Dapr.Actors;
namespace Contoso.Energy.Infrastructure.Actors;

public interface IHouseActor : IActor
{
    Task SetTemperatureAsync(double temperature);
    Task<double> GetTemperatureAsync();
    Task SetTargetTemperatureAsync(double targetTemperature);
    Task<double> GetTargetTemperatureAsync();
    Task<ThermostatStatus> GetThermostatStatusAsync();
}
