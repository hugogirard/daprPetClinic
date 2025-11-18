from contextlib import asynccontextmanager
from fastapi import FastAPI
from dapr_agents import Agent
from dapr_agents.llm import AzureOpenAIClient
from dapr_agents.agents.configs import AgentMemoryConfig
from dapr_agents.memory import ConversationDaprStateMemory
from dotenv import load_dotenv
from tools import get_appointment
from dapr.ext.fastapi import DaprApp
from dapr.aio.clients import DaprClient
import os

@asynccontextmanager
async def lifespan_event(app: FastAPI):

    app.state.dapr = DaprClient()

    # load_dotenv(override=True)

    # agent_memory_config = AgentMemoryConfig(
    #     store=ConversationDaprStateMemory(store_name="historystore",session_id="appointment")
    # )

    # agent = Agent(
    #     name="appointment-agent",
    #     role="You are an agent that help user to know about their appointment",
    #     instructions=["You are an appointment agent, you always use the get_appointment tool, if no answer provided from the tool you answer cannot find the information.  You answer only about appointment nothing else"],        
    #     memory=agent_memory_config,
    #     tools=[get_appointment]
    # )
    
    # app.state.agent = agent 

    yield


class Boostrapper:

    def run(self) -> FastAPI:

        return FastAPI(lifespan=lifespan_event)        