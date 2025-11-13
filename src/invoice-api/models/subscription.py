from pydantic import BaseModel

class Subscription(BaseModel):
    pubsubname:str
    topic:str
    route:str
