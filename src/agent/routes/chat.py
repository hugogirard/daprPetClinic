from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi import HTTPException
from dependencies import get_logger
from dapr_agents import Agent
from dapr_agents import Agent
from dapr_agents.llm import AzureOpenAIClient
from dapr_agents.agents.configs import AgentMemoryConfig
from dapr_agents.memory import ConversationDaprStateMemory
from logging import Logger
from tools import get_appointment

router = APIRouter(
    prefix="/chat"
)

@router.post('/')
async def chat(prompt:str,
               session_id:str,
               logger: Annotated[Logger, Depends(get_logger)]) -> str:
    try:

        agent_memory_config = AgentMemoryConfig(
            store=ConversationDaprStateMemory(store_name="historystore",session_id=session_id)
        )

        agent = Agent(
            name="appointment-agent",
            role="You are an agent that help user to know about their appointment",
            instructions=["You are an appointment agent, you always use the get_appointment tool, if no answer provided from the tool you answer cannot find the information.  You answer only about appointment nothing else"],        
            memory=agent_memory_config,
            tools=[get_appointment]
        )        
        
        response = await agent.run(prompt)
        return response.content
    
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail='Internal Server Error')