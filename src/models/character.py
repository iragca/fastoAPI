from pydantic import BaseModel

class Character(BaseModel):
    character_name: str
    quote: str