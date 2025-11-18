from actors import ThermostatActorInterface
from dapr.actor import ActorId, ActorProxy, ActorProxyFactory
from dapr.clients.retry import RetryPolicy
import asyncio

async def main():

    # Create proxy client
    factory = ActorProxyFactory(retry_policy=RetryPolicy(max_attempts=3))
    proxy = ActorProxy.create("ThermoActor", ActorId("home-123"), ThermostatActorInterface, factory)

    await proxy.report_temperature()