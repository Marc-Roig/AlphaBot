from typing import Optional
from telegram.ext import CallbackContext

class AlphaContext(CallbackContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_email: Optional[str] = None