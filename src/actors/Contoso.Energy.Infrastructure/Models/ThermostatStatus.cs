namespace Contoso.Energy.Infrastructure.Models;

public class ThermostatStatus
{
    public double CurrentTemperature { get; set; }

    public double TargetTemperature { get; set; }

    public bool IsHeating { get; set; }

    public bool IsCooling { get; set; }

    public DateTime LastUpdated { get; set; }

    public ThermostatStatus()
    {
    }

    public ThermostatStatus(double currentTemperature, double targetTemperature, bool isHeating, bool isCooling, DateTime lastUpdated)
    {
        CurrentTemperature = currentTemperature;
        TargetTemperature = targetTemperature;
        IsHeating = isHeating;
        IsCooling = isCooling;
        LastUpdated = lastUpdated;
    }
}
