from dapr.actor import Actor, ActorInterface, actormethod
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThermostatActorInterface(ActorInterface):
    """Interface for Quebec Winter Thermostat"""

    @actormethod(name="ReportTemperature")
    async def report_temperature(self, indoor_temp: float, outdoor_temp: float):
        pass

    @actormethod(name="SetTargetTemperature")
    async def set_target_temperature(self, target_temp: float):
        pass

    @actormethod(name="GetStatus")
    async def get_status(self) -> dict:
        pass

class QuebecThermostatActor(Actor, ThermostatActorInterface):
    """
    Simple thermostat actor for Quebec winter demo.
    Each actor = one thermostat in a Quebec home.
    """

    async def _on_activate(self) -> None:
        """Initialize the thermostat"""
        logger.info(f"🏠 Thermostat {self.id} activated")
        
        # Set defaults on first activation
        if not await self._state_manager.try_get_state("target_temp"):
            await self._state_manager.set_state("target_temp", 20.0)
            await self._state_manager.set_state("heating_on", False)

    async def report_temperature(self, indoor_temp: float, outdoor_temp: float):
        """Report temperatures and decide if heating is needed"""
        now = datetime.utcnow().isoformat()
        
        # Save reading
        reading = {
            "indoor": indoor_temp,
            "outdoor": outdoor_temp,
            "timestamp": now
        }
        await self._state_manager.set_state("last_reading", reading)
        
        # Get target and decide on heating
        target = await self._state_manager.get_state("target_temp")
        heating_on = indoor_temp < target - 1.0  # Heat if 1°C below target
        
        await self._state_manager.set_state("heating_on", heating_on)
        
        status = "🔥 HEATING" if heating_on else "✓ OK"
        logger.info(f"Thermostat {self.id}: Indoor={indoor_temp}°C, Outdoor={outdoor_temp}°C, Target={target}°C - {status}")
        
        # Alert if extreme cold outside
        if outdoor_temp < -25:
            logger.warning(f"❄️ EXTREME COLD ALERT for {self.id}: {outdoor_temp}°C outside!")

    async def set_target_temperature(self, target_temp: float):
        """Set desired temperature"""
        await self._state_manager.set_state("target_temp", target_temp)
        logger.info(f"Thermostat {self.id}: Target set to {target_temp}°C")

    async def get_status(self) -> dict:
        """Get current thermostat status"""
        reading = await self._state_manager.try_get_state("last_reading")
        target = await self._state_manager.get_state("target_temp")
        heating = await self._state_manager.get_state("heating_on")
        
        return {
            "thermostat_id": str(self.id),
            "target_temp": target,
            "heating_on": heating,
            "last_reading": reading
        }    