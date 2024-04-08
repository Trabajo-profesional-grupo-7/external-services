from pydantic import BaseModel


class Currency(BaseModel):
    base_code: str
    target_code: str
    conversion: float
