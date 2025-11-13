from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional, List
from models import InvoiceDetail, Invoice
from dapr.clients import DaprClient
import json

DAPR_STORE_NAME = "postgrepstatestore"

class InvoiceService:
    def __init__(self):
        self.dapr_client = DaprClient()
    
    def create_invoice_from_appointment(self, invoice_detail: InvoiceDetail) -> Invoice:
        """Generate invoice from completed appointment"""
        invoice_id = str(uuid4())
                
        subtotal = invoice_detail.amount
        tax = round(subtotal * 0.10, 2)  # 10% tax
        total = round(subtotal + tax, 2)
        
        invoice = Invoice(
            id=invoice_id,
            appointmentId=invoice_detail.appointment_id,
            ownerName=invoice_detail.owner_name,
            ownerEmail=invoice_detail.owner_email,
            animalName=invoice_detail.pet_name,
            issueDate=datetime.now(),
            dueDate=datetime.now() + timedelta(days=30),            
            subTotal=subtotal,
            tax=tax,
            total=total            
        )
        
        # Save to state store
        self.dapr_client.save_state(
            DAPR_STORE_NAME, 
            invoice_id, 
            json.dumps(invoice.model_dump(mode='json'))
        )
        
        print(f"Created invoice {invoice_id} for appointment {invoice_detail.appointment_id}")
        return invoice