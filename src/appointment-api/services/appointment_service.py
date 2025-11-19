from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from models import Appointment, AppointmentCreate, AppointmentSummary
from dapr.clients import DaprClient
import json

DAPR_STORE_NAME = "statestore"
PUB_SUB_STORE = "statestore"
NEW_APPOINTMENT_TOPIC = "new_appointment"
CANCEL_APPOINTMENT_TOPIC = "cancel_appointment"

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
                
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json', by_alias=True)))

        existing_appointments = self.get_appointments(appointment.owner.email)
        
        appointment_summary = AppointmentSummary(
            id=appointment.id,
            appointmentDate=appointment_data.appointment_date
        )
        
        existing_appointments.append(appointment_summary)

        # Serialize AppointmentSummary objects to dicts before saving
        self.dapr_client.save_state(
            DAPR_STORE_NAME,
            appointment.owner.email,
            json.dumps([appt.model_dump(mode='json', by_alias=True) for appt in existing_appointments])
        )
        
        return appointment
    
    def get_appointments(self, owner_email: str) -> List[AppointmentSummary]:
        """Get all appointments for a specific owner by email"""
        result = self.dapr_client.get_state(store_name=DAPR_STORE_NAME, key=owner_email)

        if not result.data:
            return []

        data = json.loads(result.data)

        # Parse each appointment dict into AppointmentSummary objects
        return [AppointmentSummary.model_validate(appt) for appt in data]
                
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get a specific appointment by ID"""
        result = self.dapr_client.get_state(store_name=DAPR_STORE_NAME, key=appointment_id)

        if not result.data:
            return None

        # Parse JSON before model validation
        data = json.loads(result.data)
        return Appointment.model_validate(data)        
    
    def charge_appointment(self, appointment_id: str) -> None:
        """Update the status of an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return None
                
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json', by_alias=True)))

        event = {
             "amount": 250,
             "appointmentId": appointment.id,
             "ownerName": appointment.owner.name,
             "ownerEmail": appointment.owner.email,
             "petName": appointment.animal.name,
             "appointmentReason": appointment.reason
        }

        self.dapr_client.publish_event(pubsub_name="pubsub",
                                       topic_name="invoice",
                                       data=json.dumps(event))
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel and delete an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return False
        
        self.dapr_client.delete_state(store_name=DAPR_STORE_NAME, key=appointment_id)
        return True
