from fastapi import FastAPI, HTTPException, Request
from typing import List
from models import InvoiceDetail, Subscription
from services import InvoiceService, EmailService
import uvicorn
import json

app = FastAPI(title="Pet Clinic Invoice API")
invoice_service = InvoiceService()
email_service = EmailService()

@app.get('/dapr/subscribe')
def subscribe():
    subscriptions:List[Subscription] = []
    subscriptions.append(Subscription(pubsubname="pubsub",topic="invoice",route="invoice"))    
    return subscriptions

@app.post('/invoice')
async def invoice(request:Request):
    
    body = await request.body()
    
    event_data = json.loads(body)
        
    # Extract the actual data from CloudEvent
    if 'data' in event_data:
        data = event_data['data']
        # If data is a string, parse it again
        if isinstance(data, str):
            data = json.loads(data)
    else:
        data = event_data

    print(f"Subscriber received invoice event: {data}", flush=True)
    
    invoice_detail = InvoiceDetail(
        amount=data['amount'],
        appointment_id=data['appointmentId'],
        owner_name=data['ownerName'],
        owner_email=data['ownerEmail'],
        pet_name=data['petName'],
        appointment_reason=data['appointmentReason']
    )

    invoice = invoice_service.create_invoice_from_appointment(invoice_detail)
        
    email_service.send_email(invoice)

    return json.dumps({'success': True})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)