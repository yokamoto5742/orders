import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import CreateOrderSchema, GetOrderSchema, GetOrdersSchema

orders = []


@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return {'orders': orders}


@app.post('/orders', status_code=status.HTTP_201_CREATED, response_model=GetOrderSchema)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.utcnow()
    order['status'] = 'created'
    orders.append(order)
    return order


@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:
        return {'orders': orders}
    query_set = [order for order in orders]

    if cancelled is not None:
        if cancelled:
            query_set = [
                order for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order for order in query_set
                if order['status'] != 'cancelled'
            ]

    if limit is not None and len(query_set) > limit:
        return {'orders': query_set[:limit]}

    return {'orders': query_set}


@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {order_id} not found')


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order['id'] == order_id:
            orders.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {order_id} not found')


@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {order_id} not found')


@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {order_id} not found')
