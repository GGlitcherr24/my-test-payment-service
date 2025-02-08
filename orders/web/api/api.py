import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.web.main import app
from orders.web.api.schemas import CreateOrderSchema, GetOrdersSchema, GetOrderSchema
from orders.orders_service.exceptions import OrderNotFoundError
from orders.orders_service.order_service import OrderService
from orders.Repository.orders_repository import OrderRepository
from orders.Repository.unit_of_work import UnitOfWork


@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    with UnitOfWork() as unit_of_work:
        repo = OrderRepository(unit_of_work.session)
        orders_service = OrderService(repo)
        results = orders_service.list_order(
            limit=limit, cancelled=cancelled
        )
        return {'orders': [result.dict() for result in results]}


@app.post('/orders', response_model=GetOrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = OrderRepository(unit_of_work.session)
        orders_service = OrderService(repo)
        order = payload.dict()["order"]
        for item in order:
            item["size"] = item["size"].value
        order = orders_service.place_order(order)
        unit_of_work.commit()
        print(order.dict())
        return_payload = order.dict()
    return return_payload


@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    try:
        with UnitOfWork as unit_of_work:
            repo = OrderRepository(unit_of_work.session)
            orders_service = OrderService(repo)
            order = orders_service.get_order(order_id=order_id)
        return order.dict()
    except:
        raise HTTPException(
            status_code=404, detail=f'Order with order_id {order_id} not found'
        )


@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrderRepository(unit_of_work.session)
            orders_service = OrderService(repo)
            order = order_details.model_dump()['order']
            for item in order:
                item['size'] = item['size'].value
            order = orders_service.update_order(order_id=order_id, items=order)
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )


@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_order(order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrderRepository(unit_of_work.session)
            order_service = OrderService(repo)
            order_service.delete_order(order_id=order_id)
            unit_of_work.commit()
        return
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )


@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrderRepository(unit_of_work.session)
            orders_service = OrderService(repo)
            order = orders_service.cancel_order(order_id=order_id)
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )


@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    try:
        with UnitOfWork() as unit_of_work:
            repo = OrderRepository(unit_of_work.session)
            orders_service = OrderService(repo)
            order = orders_service.pay_order(order_id=order_id)
            unit_of_work.commit()
        return order.dict()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Order with ID {order_id} not found"
        )
