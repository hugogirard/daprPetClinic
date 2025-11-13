from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from routes import routes
import uvicorn

app = FastAPI(title="Pet Clinic Appointment API")

for route in routes:
    app.include_router(route)

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8001)