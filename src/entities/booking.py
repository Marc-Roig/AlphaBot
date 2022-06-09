import datetime
from typing import Literal, Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class Booking(BaseModel):
    status: Literal["NONE", "QUEUED", "BOOKED", "SCHEDULED"]
    id: str
    enabled: bool
    cancel_id: Optional[str]
    class_name: Optional[str]
    occupation: int
    limit: int
    wait_list_occupation: int = Field(..., le=5)
    start_timestamp: datetime.datetime
    end_timestamp: datetime.datetime 

    def is_booked(self) -> bool:
        return self.status in ["QUEUED", "BOOKED"]
    
    def is_scheduled(self) -> bool:
        return self.status == "SCHEDULED"
       
    def has_started(self) -> bool:
        return datetime.datetime.now() > self.start_timestamp
    
    def is_inrange_to_book(self) -> bool:
        return not self.has_started() and \
                  (self.start_timestamp - datetime.datetime.now()).days < 4
    
    def is_full(self) -> bool:
        return self.wait_list_occupation >= 5

    def is_bookable(self) -> bool:        
        return not self.has_started() and \
                   self.is_inrange_to_book() and \
               not self.is_full() and \
               not self.is_booked()
    
    def get_next_bookable_date(self) -> datetime.datetime:
        # 4 days before class
        return self.start_timestamp - datetime.timedelta(days=4)

# import datetime
# from pydantic import BaseModel, Extra

# from src.shared.utils.date_transformations import int_to_datetime

# class ScheduledBooking(BaseModel, extra=Extra.ignore):
#     booking_id: str
#     mail: str
#     class_name: str
#     start_timestamp: int
#     bookable_timestamp: int
#     retries: int = 0
    
#     @property
#     def start_date(self) -> datetime.datetime:
#         date: datetime.datetime = int_to_datetime(self.start_timestamp)
#         return date