from fastapi import FastAPI
from bootstrapper import Boostrapper
from fastapi.responses import RedirectResponse
from routes import routes
import uvicorn

app = Boostrapper().run()

for route in routes:
    app.include_router(route,prefix="/api")

@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")    


if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=3100)