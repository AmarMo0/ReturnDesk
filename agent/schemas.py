from typing import Literal, Optional

from pydantic import BaseModel


class Extracted(BaseModel):
    request_type: Literal["standard_return", "damaged_replacement", "unknown"]
    order_id: Optional[str]
    item_used: Optional[bool]

CaseConfirmation = Literal["confirmed", "declined", "unclear"]


class Confirmation(BaseModel):
    decision: Literal["confirmed", "declined", "unclear"]