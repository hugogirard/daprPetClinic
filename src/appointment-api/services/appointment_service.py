from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from models import Appointment, AppointmentCreate, AppointmentSummary
from dapr.clients import DaprClient
import json

DAPR_STORE_NAME = "statestore"

class AppointmentService:
    def __init__(self):
        self.dapr_client = DaprClient()
    
    def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        """Create a new appointment for a pet"""
        appointment_id = str(uuid4())
        
        appointment = Appointment(
            id=appointment_id,
            animal=appointment_data.animal,
            owner=appointment_data.owner,
            appointment_date=appointment_data.appointment_date,
            reason=appointment_data.reason,
            notes=appointment_data.notes,            
            created_at=datetime.now()
        )
                
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json')))

        existing_appointments = self.get_appointments(appointment.owner.email)
        # Save all appointments for a client
        appointment_summary = AppointmentSummary(
            id=appointment.id,
            appointmentDate=appointment_data.appointment_date
        )
        
        
        # {
        #     "appointmentId": appointment.id,
        #     "appointmentDate": appointment.appointment_date.isoformat()
        # }        
        existing_appointments.append(appointment_summary)

        self.dapr_client.save_state(DAPR_STORE_NAME,appointment.owner.email,json.dumps(existing_appointments))
        
        return appointment
    
    def get_appointments(self, owner_email: str) -> List[AppointmentSummary]:
        """Get all appointments for a specific owner by email"""
        result = self.dapr_client.get_state(store_name=DAPR_STORE_NAME, key=owner_email)

        if not result.data:
            return []

        # Parse the result - could be a single appointment or a list
        data = json.loads(result.data)
        
        # If it's a list, parse each appointment
        return data
                
    def get_appointment(self, owner_email: str) -> Optional[Appointment]:
        """Get a specific appointment by ID"""
        result = self.dapr_client.get_state(store_name=DAPR_STORE_NAME,key=owner_email)

        if not result.data:
            return None

        return Appointment.model_validate(result.data)        
    
    def charge_appointment(self, appointment_id: str) -> None:
        """Update the status of an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return None
                
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json')))                
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel and delete an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return False
        
        self.dapr_client.delete_state(store_name=DAPR_STORE_NAME, key=appointment_id)
        return True
