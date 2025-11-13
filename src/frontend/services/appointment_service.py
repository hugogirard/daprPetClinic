from typing import List, Optional
from models import Appointment, AppointmentCreate, AppointmentStatus
from dapr.clients import DaprClient
import os
import json

APPOINTMENT_API_ID = "appointment-api"

class AppointmentService:
    """Service class to interact with the Appointment API"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.dapr_client = DaprClient()
        self.base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
                       'DAPR_HTTP_PORT', '3505')
        
        # Adding app id as part of the header
        headers = {'dapr-app-id': 'pet-clinic', 'content-type': 'application/json'}

        # self.base_url = base_url
        # self.appointments_endpoint = f"{base_url}/appointments"
    
    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        """Create a new appointment"""

        response = await self.dapr_client.invoke_method_async(app_id=APPOINTMENT_API_ID,
                                                              method_name="appointments",
                                                              data=appointment_data.model_dump(mode='json'),
                                                              http_verb="POST")

        # response = requests.post(
        #     self.appointments_endpoint,
        #     json=appointment_data.model_dump(mode='json'),
        #     headers={"Content-Type": "application/json"}
        # )
        # response.raise_for_status()
        response_data = json.loads(response.data)
        return Appointment(**response_data)
    
    def list_appointments(self, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """List all appointments, optionally filtered by status"""
        pass
        # params = {"status": status.value} if status else {}
        # response = requests.get(self.appointments_endpoint, params=params)
        # response.raise_for_status()
        # return [Appointment(**apt) for apt in response.json()]
    
    def get_appointment(self, appointment_id: str) -> Appointment:
        pass
        # """Get a specific appointment by ID"""
        # response = requests.get(f"{self.appointments_endpoint}/{appointment_id}")
        # response.raise_for_status()
        # return Appointment(**response.json())
    
    def update_appointment_status(self, appointment_id: str, status: AppointmentStatus) -> Appointment:
        pass
        # """Update the status of an appointment"""
        # response = requests.put(
        #     f"{self.appointments_endpoint}/{appointment_id}/status",
        #     params={"status": status.value}
        # )
        # response.raise_for_status()
        # return Appointment(**response.json())
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        pass
        # """Cancel and delete an appointment"""
        # response = requests.delete(f"{self.appointments_endpoint}/{appointment_id}")
        # response.raise_for_status()
        # return True
