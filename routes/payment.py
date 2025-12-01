from datetime import datetime
from config.db import db
from fastapi import APIRouter, HTTPException
from models.payment import Payment
from schemas.payment import paymentEntity, paymentsEntity
from bson import ObjectId # type: ignore

payment = APIRouter(prefix="/payments", tags=["Payments"])

# Create
@payment.post('')
def create_payment(orderId: str,method: str, payment_data: Payment): #Done
    #validar si la orden existe
    order_data = db.order.find_one({"_id": ObjectId(orderId)})
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")
    #validar si ya existe un pago para esta orden
    existing_payment = db.payment.find_one({"orderId": orderId})
    if existing_payment:
        raise HTTPException(status_code=400, detail="Payment already exists for this order")
    payment = dict(payment_data)
    payment['orderId'] = orderId
    payment['paymentMethod'] = method
    payment['paymentDate'] = datetime.now()
    payment['status'] = "completed"
    payment['amount'] = order_data['totalAmount']
    result = db.payment.insert_one(payment)
    payment['id'] = str(result.inserted_id)
    return {"id": str(result.inserted_id)}

# Research
@payment.get('')
def get_payments(): #Done
    return paymentsEntity(db.payment.find())

@payment.get('/{payment_id}')
def get_payment_by_id(payment_id: str): #Done
    return paymentEntity(db.payment.find_one({"_id": ObjectId(payment_id)}))

@payment.get('/order/{order_id}')
def get_payment_by_order(order_id: str): #Done
    return paymentEntity(db.payment.find_one({"order_id": order_id}))

# Update
@payment.put('/{payment_id}/status')
def update_payment_status(payment_id: str, status: str): #Done
    news = ["pending", "completed", "failed", "refunded"]
    if status not in news:
        raise HTTPException(status_code=400, detail="Invalid status value")
    db.payment.update_one({"_id": ObjectId(payment_id)}, {"$set": {"status": status}})
    return get_payment_by_id(payment_id)

@payment.put('/{payment_id}/method')
def update_payment_method(payment_id: str, method: str): #Done
    db.payment.update_one({"_id": ObjectId(payment_id)}, {"$set": {"paymentMethod": method}})
    return get_payment_by_id(payment_id)

# Delete
@payment.delete('/{payment_id}')
def delete_payment(payment_id: str):
    db.payment.delete_one({"_id": ObjectId(payment_id)})
    return {"message": "Payment deleted successfully"}
