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
    #validar si no hay ordenes "creating" con este userId
    existing_order = db.order.find_one({"userId": userId, "status": "creating"})
    if existing_order:
        raise HTTPException(status_code=400, detail="There is already an order in 'creating' status for this user")
    order = dict(order_data)
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
def get_orders(): #Done
    return ordersEntity(db.order.find())

@order.get('/user/{user_id}')
def get_orders_by_user(user_id: str): #Done
    return ordersEntity(db.order.find({"userId": user_id}))

@order.get('/{order_id}')
def get_order_by_id(order_id: str):
    order_data = db.order.find_one({"_id": ObjectId(order_id)})
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")
    return orderEntity(order_data)


# Update
@order.put('/{order_id}/status')
def update_order_status(order_id: str, status: str):
    return {"order_id": order_id, "status": status}


# Delete
@order.delete('/{order_id}')
def delete_order(order_id: str):
    return {"order_id": order_id}