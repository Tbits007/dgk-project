from pydantic import BaseModel


class ActionSchema(BaseModel):
    email: str
    action_type: str
    details: str | None = None