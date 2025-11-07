from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.user import User
from schemas.user import userEntity,usersEntity
from config.db import db
from bson import ObjectId # type: ignore

user = APIRouter(prefix="/users", tags=["Users"])

# Crate
    #Crear Usuarios
@user.post('')
def create_user(user: User):
    now = datetime.utcnow()
    obj_id = ObjectId()
    user_dict = user.dict(exclude_none=True)
    user_dict["_id"] = obj_id            # Mongo _id (ObjectId)
    user_dict["id"] = str(obj_id)       # campo string que usaremos como referencia
    user_dict["createdAt"] = now
    user_dict["updatedAt"] = now

    db.users.insert_one(user_dict)
    user_dict.pop("_id")  # opcional: no devolver ObjectId en la respuesta
    return user_dict

# Research

@user.get('')
def get_users():
    return usersEntity(db.user.find())

@user.get('/{user_id}')
def get_user_by_id(user_id: str):
    user_data = db.user.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return userEntity(user_data)

@user.get('/email/{email}')
def get_user_by_email(email: str):
    return email

# Update

@user.put('/{user_id}/password')
def update_user_password(user_id: str, new_password: str):
    return {"user_id": user_id, "new_password": new_password}

@user.put('/{user_id}/profile')
def update_user_profile(user_id: str, user: dict):
    updated_data = {**user.dict(), "updatedAt": datetime.utcnow()}
    result = db.user.update_one(
        {"_id": ObjectId(user_id)},
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

# Auth
@user.post('/auth/login')
def login_user(email: str, password: str):
    return {"email": email, "password": password}

@user.post('/auth/recover')
def recover_password(email: str):
    return email

@user.post('/auth/reset')
def reset_password(token: str, new_password: str):
    return {"token": token, "new_password": new_password}