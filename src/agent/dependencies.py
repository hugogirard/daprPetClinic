from fastapi import FastAPI
from fastapi import Request, HTTPException
from logging import Logger
from dapr_agents import Agent
from dapr.aio.clients import DaprClient
import logging
import sys

_logger = logging.getLogger('agentapi')

_logger.setLevel(logging.DEBUG)

# StreamHandler for the console
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
_logger.addHandler(stream_handler)

# ####################################
# Dependency methods using dependency 
# injection in the route
######################################

def get_agent(request:Request) -> Agent:
    return request.app.state.agent

def get_logger() -> Logger:
    return _logger

def get_dapr_client(request:Request) -> DaprClient:
    return request.app.state.dapr