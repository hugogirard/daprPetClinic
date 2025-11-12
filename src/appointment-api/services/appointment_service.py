from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from models import Appointment, AppointmentCreate, AppointmentStatus
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem
from dapr.clients.grpc._request import TransactionalStateOperation, TransactionOperationType
import json

DAPR_STORE_NAME = "statestore"

class AppointmentService:
    def __init__(self):
        #self.appointments_db: dict[str, Appointment] = {}
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
            status=AppointmentStatus.SCHEDULED,
            created_at=datetime.now()
        )
        
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json')))

        #self.appointments_db[appointment_id] = appointment
        return appointment
    
    def list_appointments(self, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """List all appointments, optionally filtered by status"""
        query = {
            "filter": {},
            "sort": []
        }
        
        if status:
            query["filter"] = {
                "EQ": {"status": status.value}
            }
        
        results = self.dapr_client.query_state(
            store_name=DAPR_STORE_NAME,
            query=json.dumps(query)
        )
        
        appointments = []
        for item in results.results:
            appointments.append(Appointment.model_validate(json.loads(item.value)))
        
        return appointments

        # if status:
        #     return [apt for apt in self.appointments_db.values() if apt.status == status]
        # return list(self.appointments_db.values())
    
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get a specific appointment by ID"""
        result = self.dapr_client.get_state(store_name=DAPR_STORE_NAME,key=appointment_id)

        if not result.data:
            return None

        return Appointment.model_validate(result.data)
        #return self.appointments_db.get(appointment_id)
    
    def update_appointment_status(self, appointment_id: str, status: AppointmentStatus) -> Optional[Appointment]:
        """Update the status of an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return None
        
        appointment.status = status
        self.dapr_client.save_state(DAPR_STORE_NAME, appointment_id, json.dumps(appointment.model_dump(mode='json')))
        
        return appointment
        #self.appointments_db[appointment_id].status = status
        #return self.appointments_db[appointment_id]
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel and delete an appointment"""

        appointment = self.get_appointment(appointment_id)
        
        if not appointment:
            return False
        
        self.dapr_client.delete_state(store_name=DAPR_STORE_NAME, key=appointment_id)
        return True
        # if appointment_id not in self.appointments_db:
        #     return False
            
        # self.appointments_db[appointment_id].status = AppointmentStatus.CANCELLED
        # del self.appointments_db[appointment_id]
        # return True
