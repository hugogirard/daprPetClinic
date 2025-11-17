```
from dapr.actor import Actor, ActorInterface, actormethod
from datetime import datetime, timedelta

HEARTBEAT_TIMER_NAME = "heartbeat_checker"


class DeviceTelemetryInterface(ActorInterface):

    @actormethod(name="ReportTelemetry")
    async def report_telemetry(self, temperature: float, battery: float):
        pass

    @actormethod(name="GetStatus")
    async def get_status(self) -> dict:
        pass

    @actormethod(name="EnableHeartbeat")
    async def enable_heartbeat(self, interval_seconds: int):
        pass

    @actormethod(name="DisableHeartbeat")
    async def disable_heartbeat(self):
        pass


class DeviceTelemetryActor(Actor, DeviceTelemetryInterface):
    """
    One actor = one device
    Stores last telemetry + checks heartbeat timer
    """

    LAST_TELEMETRY_KEY = "last_telemetry"
    LAST_HEARTBEAT_KEY = "last_heartbeat"
    STATUS_KEY = "device_status"

    async def on_activate(self):
        # Init status on first activation
        await self._state_manager.set_state(self.STATUS_KEY, "offline")

    # --- PUBLIC METHODS -----------------------------------------------------

    async def report_telemetry(self, temperature: float, battery: float):
        now = datetime.utcnow().isoformat()

        # Save telemetry
        telemetry = {
            "temperature": temperature,
            "battery": battery,
            "timestamp": now
        }

        await self._state_manager.set_state(self.LAST_TELEMETRY_KEY, telemetry)
        await self._state_manager.set_state(self.LAST_HEARTBEAT_KEY, now)
        await self._state_manager.set_state(self.STATUS_KEY, "online")

    async def get_status(self) -> dict:
        telemetry = await self._state_manager.get_state(self.LAST_TELEMETRY_KEY)
        status = await self._state_manager.get_state(self.STATUS_KEY)
        last_seen = await self._state_manager.get_state(self.LAST_HEARTBEAT_KEY)

        return {
            "status": status,
            "last_seen": last_seen,
            "telemetry": telemetry
        }

    async def enable_heartbeat(self, interval_seconds: int):
        # Timer that checks if device is still online
        await self.register_timer(
            timer_name=HEARTBEAT_TIMER_NAME,
            callback=self._check_heartbeat,
            due_time=interval_seconds,
            period=interval_seconds
        )

    async def disable_heartbeat(self):
        await self.unregister_timer(HEARTBEAT_TIMER_NAME)

    # --- INTERNAL TIMER CALLBACK --------------------------------------------

    async def _check_heartbeat(self):
        """
        Timer runs every X seconds.
        If device hasn't reported telemetry recently → mark offline.
        """
        last_seen = await self._state_manager.get_state(self.LAST_HEARTBEAT_KEY)

        if last_seen:
            last_seen_dt = datetime.fromisoformat(last_seen)
            delta = datetime.utcnow() - last_seen_dt

            if delta > timedelta(seconds=30):  # configurable threshold  
                await self._state_manager.set_state(self.STATUS_KEY, "offline")

```
