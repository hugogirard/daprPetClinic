from dapr_agents import tool
from dapr.clients import DaprClient
from models import Appointment
import json

dapr = DaprClient()

DAPR_STORE_NAME = "statestore"

@tool
def get_appointment(email:str) -> str:
    """
    get_appointment(email: str) -> str:
        Tool to retrieve appointment details for a given user's email address.
        This function is intended to be used as part of the Dapr agent's toolset
        for interacting with appointment data in the pet clinic application.
        Args:
            email (str): The email address of the user whose appointment information is requested.
        Returns:
            Appointment: A class that contains all the appointment information.
    """

    response = dapr.get_state(
        store_name=DAPR_STORE_NAME,
        key=email,
        state_metadata={"appid": "appointment-api"}
    )  

    if not response.data:
        return f"No appointment found for email: {email}"

    return response.data.decode('utf-8') if isinstance(response.data, bytes) else str(response.data)  