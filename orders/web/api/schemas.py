from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, NonNegativeInt, model_validator


class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class Status(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: NonNegativeInt = Field(default=1, gt=0)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def quantity_non_nullable(self):
        assert self.quantity is not None, "quantity may not be None"
        return self


class CreateOrderSchema(BaseModel):
    order: List[OrderItemSchema] = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: Status


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]

    model_config = ConfigDict(extra="forbid")
