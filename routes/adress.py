import datetime
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
    address_dict = address_data.dict()
    address_dict["userid"] = userId
    result = db.address.insert_one(address_dict)
    new_address = db.address.find_one({"_id": result.inserted_id})
    return addressEntity(new_address)


# Research
@address.get('')
def get_addresses(): #Done
    return addressesEntity(db.address.find())

@address.get('/{address_id}')
def get_address_by_id(address_id: str): #Done
    if len(address_id) != 24:
        raise HTTPException(status_code=400, detail="ID de dirección inválido")
    address_data = db.address.find_one({"_id": ObjectId(address_id)})
    if not address_data:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return addressEntity(address_data)

@address.get('/user/{user_id}') #Done
def get_addresses_by_user(user_id: str):
    if len(user_id) != 24:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    addresses = addressesEntity(db.address.find({"userid": user_id}))
    return addresses

# Update
@address.put('/{address_id}')
def update_address(address_id: str, address_data: Address): #Done
    if len(address_id) != 24:
        raise HTTPException(status_code=400, detail="ID de dirección inválido")
    result = db.address.update_one(
        {"_id": ObjectId(address_id)},
        {"$set": address_data.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    updated_address = db.address.find_one({"_id": ObjectId(address_id)})
    return addressEntity(updated_address)

# Delete
@address.delete('/{address_id}')
def delete_address(address_id: str):
    db.address.delete_one({"_id": ObjectId(address_id)})
    return {"message": "Address deleted successfully"}