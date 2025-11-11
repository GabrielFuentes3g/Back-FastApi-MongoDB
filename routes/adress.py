from http.client import HTTPException
from config.db import db
from fastapi import APIRouter
from models.address import Address
from schemas.address import addressEntity, addressesEntity
from bson import ObjectId # type: ignore

address = APIRouter(prefix="/addresses", tags=["Addresses"])

# Create
@address.post('')
def create_address(userId: str, address_data: Address): #Done
    if len(userId) != 24:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    user_data = db.user.find_one({"_id": ObjectId(userId)})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    address_dict = dict(address_data)
    address_dict["userId"] = userId
    result = db.address.insert_one(address_dict)
    new_address = db.address.find_one({"_id": result.inserted_id})
    return addressEntity(new_address)
# Research
@address.get('')
def get_addresses():
    return addressesEntity(db.address.find())

@address.get('/{address_id}')
def get_address_by_id(address_id: str):
    return addressEntity(db.address.find_one({"_id": ObjectId(address_id)}))

@address.get('/user/{user_id}')
def get_addresses_by_user(user_id: str):
    return addressesEntity(db.address.find({"user_id": user_id}))

# Update
@address.put('/{address_id}')
def update_address(address_id: str, address_data: Address):
    db.address.update_one({"_id": ObjectId(address_id)}, {"$set": address_data.dict()})
    return addressEntity(address_data)

# Delete
@address.delete('/{address_id}')
def delete_address(address_id: str):
    db.address.delete_one({"_id": ObjectId(address_id)})
    return {"message": "Address deleted successfully"}