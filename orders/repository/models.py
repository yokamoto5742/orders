import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(String, primary_key=True, default=generate_uuid)
    items = relationship('OrderItemModel', back_populates='order')
    status = Column(String, default='pending')
    created = Column(DateTime, default=datetime.utcnow)
    scheduled_id = Column(String)
    delivery_id = Column(String)

    def dict(self):
        return {
            'id': self.id,
            'items': [item.dict() for item in self.items],
            'status': self.status,
            'created': self.created,
            'scheduled_id': self.scheduled_id,
            'delivery_id': self.delivery_id
        }


class OrderItemModel(Base):
    __tablename__ = 'order_items'

    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product = Column(String, nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }
