from datetime import datetime

from pydantic import BaseModel
from dataclasses import dataclass

# class YoomoneyOperation(BaseModel):


@dataclass
class YoomoneyOperation:
    operation_id: str
    status: str  # Can be: success / refused / in_progress.
    datetime: datetime
    title: str
    pattern_id: str
    direction: str  # Can be: in / out.
    amount: float
    label: str | None
    type: str  # Can be: payment-shop / outgoing-transfer / deposition / incoming-transfer.
