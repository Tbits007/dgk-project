from dataclasses import dataclass


@dataclass(slots=True)
class ActionDM:
    email: str
    action_type: str
    details: str
    
    _id: str | None = None

