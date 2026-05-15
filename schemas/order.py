from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItemBase(BaseModel):
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemBase]
    total_price: float
    delivery_address: str

class OrderUpdate(BaseModel):
    items: Optional[List[OrderItemBase]] = None
    total_price: Optional[float] = None
    delivery_address: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: int
    user_id: int
    items: str
    total_price: float
    status: OrderStatus
    delivery_address: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
