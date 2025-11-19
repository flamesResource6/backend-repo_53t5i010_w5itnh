from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

# Each Pydantic model corresponds to a MongoDB collection (lowercased class name)

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    slug: str
    price: float
    images: List[HttpUrl] = []
    description: Optional[str] = None
    sizes: List[str] = ["XS", "S", "M", "L", "XL"]
    colors: List[str] = ["Black", "White", "Navy"]
    featured: bool = False
    tags: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True

class CartItem(BaseModel):
    product_id: str
    size: Optional[str] = None
    color: Optional[str] = None
    quantity: int = 1

class Order(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    items: List[CartItem]
    total: float
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
