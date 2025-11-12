from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from models import Appointment, AppointmentCreate, AppointmentStatus


class AppointmentService:
    def __init__(self):
        self.appointments_db: dict[str, Appointment] = {}
    
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
        
        self.appointments_db[appointment_id] = appointment
        return appointment
    
    def list_appointments(self, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """List all appointments, optionally filtered by status"""
        if status:
            return [apt for apt in self.appointments_db.values() if apt.status == status]
        return list(self.appointments_db.values())
    
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get a specific appointment by ID"""
        return self.appointments_db.get(appointment_id)
    
    def update_appointment_status(self, appointment_id: str, status: AppointmentStatus) -> Optional[Appointment]:
        """Update the status of an appointment"""
        if appointment_id not in self.appointments_db:
            return None
        
        self.appointments_db[appointment_id].status = status
        return self.appointments_db[appointment_id]
    
    def cancel_appointment(self, appointment_id: str) -> bool:
        """Cancel and delete an appointment"""
        if appointment_id not in self.appointments_db:
            return False
        
        self.appointments_db[appointment_id].status = AppointmentStatus.CANCELLED
        del self.appointments_db[appointment_id]
        return True
