from pydantic import BaseModel, Field
from typing import Optional, List

# --- Схемы для эндпоинта /upload/ ---

class Prediction(BaseModel):
    IMG: str
    type: str
    date: str
    size: str
    confidence: str
    passport: Optional[int] = None

class UploadResponse(BaseModel):
    pred: List[Prediction]
    diagram: dict[str, int]

# --- Схемы для паспортов ---

class PassportBase(BaseModel):
    age: int
    gender: str
    name: str

class PassportCreate(PassportBase):
    cords_sd: float = Field(..., description="Широта")
    cords_vd: float = Field(..., description="Долгота")

class PassportInDB(PassportBase):
    id: int
    image_preview: Optional[str] = None
    type: str

    class Config:
        # Позволяет Pydantic работать с объектами БД напрямую
        from_attributes = True
