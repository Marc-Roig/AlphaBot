import datetime
from typing import Literal, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class Booking(BaseModel):
    status: Literal["NONE", "QUEUED", "BOOKED", "SCHEDULED", "CANCELED"]
    id: str
    enabled: bool
    cancel_id: Optional[str]
    class_name: Optional[str]
    occupation: int
    limit: int
    wait_list_occupation: int
    start_timestamp: datetime.datetime
    end_timestamp: datetime.datetime 

    def is_booked(self) -> bool:
        return self.status in ["QUEUED", "BOOKED"]
    
    def is_scheduled(self) -> bool:
        return self.status == "SCHEDULED"
    
    def is_canceled(self) -> bool:
        return self.status == "CANCELED"
       
    def has_started(self) -> bool:
        return datetime.datetime.now() > self.start_timestamp
    
    def is_in_range_to_book(self) -> bool:
        return not self.has_started() and \
                  (self.start_timestamp - datetime.datetime.now()).days < 4
    
    def is_full(self) -> bool:
        return self.wait_list_occupation >= 5

    def is_bookable(self) -> bool:        
        return not self.has_started() and \
                   self.is_in_range_to_book() and \
               not self.is_full() and \
               not self.is_booked()
    
    def get_next_bookable_date(self) -> datetime.datetime:
        # 4 days before class
        return (self.start_timestamp - datetime.timedelta(days=4)).replace(second=0, microsecond=0)

