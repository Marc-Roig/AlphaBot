from pydantic import BaseModel, Field
import datetime


class User(BaseModel):
    email: str
    token: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
