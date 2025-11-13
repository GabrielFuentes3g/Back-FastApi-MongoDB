import datetime
from config.db import db
from fastapi import APIRouter, HTTPException
from models.order import Order, OrderItem
from routes import product
from schemas.order import orderEntity, ordersEntity

order = APIRouter(prefix="/orders", tags=["Orders"])

# Create
@order.post('')
def create_order(order_data: Order, itemsIdAndQuantity: dict, userid: str, orderdate: str):
    for item_id in itemsIdAndQuantity:
        order_data.items.append(create_order_items(itemsIdAndQuantity[item_id]['productId'], itemsIdAndQuantity[item_id]['quantity'], order_data))
    #validar el user id
    if len(userid) != 24:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    order_data.userid = userid
    order_data.orderDate = orderdate
    order_data.status = "Pending"
    order_data.totalAmount = sum(item.subtotal for item in order_data.items)
    order_data.createdAt = datetime.datetime.now()
    order_data.updatedAt = datetime.datetime.now()
    result = db.order.insert_one(order_data.dict())
    return {"order_id": str(result.inserted_id)}
    

# @order.post('/{order_id}/items')
def create_order_items(productId: str, quantity: int, order: OrderItem):
    product_data = db.product.find_one({"_id": productId})
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")
    name = product_data['name']
    price = product_data['price']
    subtotal = price * quantity
    order_item = OrderItem(
        productid=productId,
        name=name,
        price=price,
        quantity=quantity,
        subtotal=subtotal
    )
    return order_item

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

@order.get('/{order_id}/items')
def get_order_items(order_id: str):
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