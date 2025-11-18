from fastapi import FastAPI, Depends
from bootstrapper import Boostrapper
from dapr.ext.fastapi import DaprApp
from fastapi.responses import RedirectResponse
from routes import routes
from models import CloudEvent, Appointment
from dependencies import get_dapr_client
from typing import List, Annotated
from dapr.aio.clients import DaprClient
import uvicorn
import json

DAPR_STORE_NAME = "statestore"

app = Boostrapper().run()

# for route in routes:
#     app.include_router(route,prefix="/api")

dapr_app = DaprApp(app)

dapr_client = DaprClient()

@dapr_app.subscribe(pubsub="pubsub",topic="new_appointment")
async def appointments_subscriber(event: CloudEvent,
                                  dapr_client: Annotated[DaprClient,Depends(get_dapr_client)]):
    
    appointment = Appointment.model_validate(event.data)   

    appointments:List[Appointment] = []

    result = await dapr_client.get_state(DAPR_STORE_NAME, appointment.email)

    if result.data:
      data = json.loads(result.data)
      appointments = [Appointment.model_validate(appt) for appt in data]

    appointments.append(appointment)

    await dapr_client.save_state(DAPR_STORE_NAME,
                                 appointment.email,                                
                                 json.dumps([a.model_dump(by_alias=True) for a in appointments]))

@dapr_app.subscribe(pubsub="pubsub",topic="cancel_appointment")
async def appointments_subscriber(event: CloudEvent,
                                  dapr_client: Annotated[DaprClient,Depends(get_dapr_client)]):
    
    appointment_id = event.data['id']
    email = event.data['email']
    
    result = await dapr_client.get_state(DAPR_STORE_NAME, email)
 
    if not result:
        return
    
    data = json.loads(result.data)
    appointments = [Appointment.model_validate(appt) for appt in data]

    # Remove the appointment with matching id
    appointments = [appt for appt in appointments if appt.id != appointment_id]

    if len(appointments) == 0:
        await dapr_client.delete_state(DAPR_STORE_NAME,email)
    else:
        # Save updated list
        await dapr_client.save_state(DAPR_STORE_NAME,
                                    email,                                
                                    json.dumps([a.model_dump(by_alias=True) for a in appointments]))

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")    

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=3100)