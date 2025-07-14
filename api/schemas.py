from pydantic import BaseModel

class ProductCount(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    date: str
    count: int

class MessageResult(BaseModel):
    message_id: int
    content: str
