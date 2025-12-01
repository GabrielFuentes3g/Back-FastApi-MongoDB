import datetime
from typing import Optional
from unittest import result

from fastapi.params import Query
from config.db import db
from fastapi import APIRouter, HTTPException
from models.order import Order
from schemas.order import orderEntity, ordersEntity
from bson import ObjectId # type: ignore


order = APIRouter(prefix="/orders", tags=["Orders"])

# Create
@order.post('')
def create_order(userId: str, order_data: Order ): #Done
    #validar si el usuario existe
    user_data = db.user.find_one({"_id": ObjectId(userId)})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")


    order = dict(order_data)
    order
    id: Optional[str] = None
    order['userId'] = userId
    order['orderDate'] = datetime.datetime.now()
    order['status'] = "creating"
    order['totalAmount'] = 0.0
    order['createdAt'] = datetime.datetime.now()
    order['updatedAt'] = datetime.datetime.now()

    result = db.order.insert_one(order)
    order['id'] = str(result.inserted_id)
    return {"id": str(result.inserted_id)}


# Research
@order.get('')
def get_orders():
    return ""

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
@order.delete('/{order_id}/itemsId')
def delete_order_items(order_id: str):
    return {"order_id": order_id}

@order.delete('/{order_id}')
def delete_order(order_id: str):
    return {"order_id": order_id}