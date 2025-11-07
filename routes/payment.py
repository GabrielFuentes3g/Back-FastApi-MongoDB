from config.db import db
from fastapi import APIRouter
from models.payment import Payment
from schemas.payment import paymentEntity, paymentsEntity
from bson import ObjectId # type: ignore

payment = APIRouter(prefix="/payments", tags=["Payments"])

# Create
@payment.post('')
def create_payment(payment_data: Payment):
    return paymentEntity(payment_data)

# Research
@payment.get('')
def get_payments():
    return paymentsEntity(db.payment.find())

@payment.get('/{payment_id}')
def get_payment_by_id(payment_id: str):
    return paymentEntity(db.payment.find_one({"_id": ObjectId(payment_id)}))

@payment.get('/order/{order_id}')
def get_payments_by_order(order_id: str):
    return paymentsEntity(db.payment.find({"order_id": order_id}))

# Update
@payment.put('/{payment_id}/status')
def update_payment_status(payment_id: str, status: str):
    return {"payment_id": payment_id, "status": status}

@payment.put('/{payment_id}/method')
def update_payment_method(payment_id: str, method: str):
    return {"payment_id": payment_id, "method": method}

# Delete
@payment.delete('/{payment_id}')
def delete_payment(payment_id: str):
    db.payment.delete_one({"_id": ObjectId(payment_id)})
    return {"message": "Payment deleted successfully"}
