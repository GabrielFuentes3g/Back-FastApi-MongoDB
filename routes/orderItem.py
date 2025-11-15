from unittest import result
from config.db import db
from fastapi import APIRouter, HTTPException
from models.orderItem import OrderItem
from schemas.orderItem import orderItemEntity, orderItemsEntity
from bson import ObjectId # type: ignore

orderItem = APIRouter(prefix="/orderItems", tags=["OrderItems"])


#create
@orderItem.post('/{orderItem_id}/items') 
def create_order_item(productId: str, quantity: int, order_data: OrderItem): #Done
    product_data = db.product.find_one({"_id": ObjectId(productId)})
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    order_item = dict(order_data)
    order_item['productId'] = productId
    order_item['name'] = product_data['name']
    order_item['quantity'] = quantity
    order_item['price'] = product_data['price']
    order_item['subtotal'] = order_item['price'] * quantity
    result = db.orderItem.insert_one(order_item)
    order_item['id'] = str(result.inserted_id)
    return {"id": str(result.inserted_id)}


#research
@orderItem.get('/{orderItem_id}/items') #Done
def get_order_items_by_id(orderItem_id: str): 
    orderItem_data = db.orderItem.find_one({"_id": ObjectId(orderItem_id)})
    if not orderItem_data:
        raise HTTPException(status_code=404, detail="Order item no encontrado")
    return orderItemEntity(orderItem_data)

@orderItem.get('/items') #Done
def get_order_items():
    return orderItemsEntity(db.orderItem.find())


#update
@orderItem.put('/items/{item_id}/quantity')
def update_order_item_quantity(item_id: str, quantity: int): #Done
    orderItem_data = db.orderItem.find_one({"_id": ObjectId(item_id)})
    if not orderItem_data:
        raise HTTPException(status_code=404, detail="Order item not found")
    subtotal = orderItem_data['price'] * quantity
    db.orderItem.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"quantity": quantity, "subtotal": subtotal}}
    )
    return get_order_items_by_id(item_id)

#delete
@orderItem.delete('/items/{item_id}')
def delete_order_item(item_id: str): #Done
    orderItem_data = db.orderItem.find_one({"_id": ObjectId(item_id)})
    if not orderItem_data:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.orderItem.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Order item deleted successfully"}