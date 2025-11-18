from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi import HTTPException
from dependencies import get_agent, get_logger
from dapr_agents import Agent
from logging import Logger

router = APIRouter(
    prefix="/appointment"
)

@router.post('/')
async def chat(prompt:str,
              session_id: str,  # Add session_id as a parameter
              agent: Annotated[Agent, Depends(get_agent)],
              logger: Annotated[Logger, Depends(get_logger)]) -> str:
    try:
        
        
        response = await agent.run(prompt)
        return response.content
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail='Internal Server Error')