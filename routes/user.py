from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.user import User
from schemas.user import userEntity,usersEntity
from config.db import db
from bson import ObjectId

user = APIRouter()

# Crate
@user.post('/users/')
def create_user(user: User):
    new_user = dict(user)
    result = db.user.insert_one(new_user)
    created_user = db.user.find_one({"_id": result.inserted_id})
    return userEntity(created_user)

# Research
@user.get('/users/{id}')
def find_user(id: str):
    user_data = db.user.find_one({"_id": ObjectId(id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return userEntity(user_data)

@user.get('/users')
def find_all_users():
    return usersEntity(db.user.find())

# Update
@user.put('/users/{id}')
def update_user(id: str, user: user):
    updated_data = {**user.dict(), "updatedAt": datetime.utcnow()}
    result = db.user.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return {"message": "usuario actualizado correctamente"}

# Delete
@user.delete('/users/{id}')
def delete_user(id: str):
    result = db.user.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    return {"message": "usuario eliminado correctamente"}