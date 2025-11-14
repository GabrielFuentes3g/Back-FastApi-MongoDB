import datetime
from unittest import result
from config.db import db
from fastapi import APIRouter, HTTPException
from models.order import Order
from schemas.order import orderEntity, ordersEntity
from bson import ObjectId # type: ignore


order = APIRouter(prefix="/orders", tags=["Orders"])

# Create
@order.post('')
def create_order(order_data: Order, itemsIdAndQuantity: dict, userid: str, orderdate: str):
    return ""


# Research
@order.get('')
def get_orders():
    return db.order.find()

@order.get('/user/{user_id}')
def get_orders_by_user(user_id: str):
    return {"user_id": user_id}

@order.get('/{order_id}')
def get_order_by_id(order_id: str):
    return {"order_id": order_id}


# Update
@order.put('/{order_id}/status')
def update_order_status(order_id: str, status: str):
    return {"order_id": order_id, "status": status}

@order.put('/{order_id}/total')
def update_order_total(order_id: str, total: float):
    return {"order_id": order_id, "total": total}

# Delete
@order.delete('/{order_id}/items')
def delete_order_items(order_id: str):
    return {"order_id": order_id}

@order.delete('/{order_id}')
def delete_order(order_id: str):
    return {"order_id": order_id}