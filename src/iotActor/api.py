from dapr.actor.runtime.runtime import ActorRuntime
from models import TempReport, TargetTemp
from actors import QuebecThermostatActor, ThermostatActorInterface
from contextlib import asynccontextmanager
from dapr.ext.fastapi import DaprActor
from fastapi import FastAPI

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Quebec Thermostat Demo")

# Add Dapr Actor Extension
actor = DaprActor(app)

@asynccontextmanager
async def lifespan_event(app: FastAPI):
    """Register actor with Dapr"""    
    await actor.register_actor(QuebecThermostatActor)
    logger.info("✓ Quebec Thermostat Actor registered")

    yield
    

# @app.on_event("startup")
# async def startup():
#     """Register actor with Dapr"""
#     ActorRuntime.register_actor(QuebecThermostatActor)
#     logger.info("✓ Quebec Thermostat Actor registered")

@app.get("/")
def home():
    return {"service": "Quebec Winter Thermostat", "status": "running"}


@app.post("/thermostat/{id}/temperature")
async def report_temp(id: str, report: TempReport):
    """Report temperature"""
    proxy = ActorRuntime.get_actor_proxy(
        actor_type="QuebecThermostatActor",
        actor_id=id,
        actor_interface=ThermostatActorInterface
    )
    await proxy.report_temperature(report.indoor_temp, report.outdoor_temp)
    return {"status": "ok"}


@app.post("/thermostat/{id}/target")
async def set_target(id: str, target: TargetTemp):
    """Set target temperature"""
    proxy = ActorRuntime.get_actor_proxy(
        actor_type="QuebecThermostatActor",
        actor_id=id,
        actor_interface=ThermostatActorInterface
    )
    await proxy.set_target_temperature(target.target_temp)
    return {"status": "ok"}


@app.get("/thermostat/{id}/status")
async def get_status(id: str):
    """Get thermostat status"""
    proxy = ActorRuntime.get_actor_proxy(
        actor_type="QuebecThermostatActor",
        actor_id=id,
        actor_interface=ThermostatActorInterface
    )
    return await proxy.get_status()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)