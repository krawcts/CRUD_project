from pydantic import BaseModel, PositiveFloat, EmailStr, field_validator
from enum import Enum
from datetime import datetime
from typing import Optional

class CategoryBase(Enum):
    category1 = "Eletronics"
    category2 = "Household Appliance"
    category3 = "Furnite"
    category4 = "Clothes"
    category5 = "Shoes"

class ProductBase(BaseModel):
    name: str
    description: str
    price: PositiveFloat
    category: str
    supplier_email: EmailStr

    @field_validator("category")
    def check_category(cls, v):
        if v in [item.value for item in CategoryBase]:
            return v
        raise ValueError("Invalid category")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    category: Optional[str] = None
    supplier_email: Optional[EmailStr] = None

    @field_validator("category", pre=True, always=True)
    def check_category(cls, v):
        if v is None:
            return v
        if v in [item.value for item in CategoryBase]:
            return v
        raise ValueError("Invalid category")