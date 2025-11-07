from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.user import User
from schemas.user import userEntity,usersEntity
from config.db import db
from bson import ObjectId # type: ignore

user = APIRouter(prefix="/users", tags=["Users"])

# Crate
@user.post('') #Done
def create_user(user: User):

#validar si el email ya existe
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    else:
        new_user = dict(user)
        result = db.user.insert_one(new_user)
        created_user = db.user.find_one({"_id": result.inserted_id})
        db.users.insert_one(created_user)
        return {"message": "Usuario creado correctamente"}

# Research

@user.get('') #Done
def get_users():
    return usersEntity(db.user.find())

@user.get('/{user_id}') #Done
def get_user_by_id(user_id: str):
    user_data = db.user.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return userEntity(user_data)

@user.get('/email/{email}')
def get_user_by_email(email: str): #Done
    user_data = db.user.find_one({"email": email})
    if not user_data:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return userEntity(user_data)

# Update

@user.put('/{user_id}/password') 
def update_user_password(user_id: str, new_password: str): #Done
    result = db.user.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": new_password, "updatedAt": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return {"message": "contraseña actualizada correctamente"}

@user.put('/{user_id}/profile')
def update_user_profile(user_id: str, user: dict): #Done
    update_data = {k: v for k, v in user.items() if k in ["firstname", "lastname", "email"]}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos válidos para actualizar")
    
    update_data["updatedAt"] = datetime.utcnow()
    
    result = db.user.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    return {"message": "perfil de usuario actualizado correctamente"}

# Delete
@user.delete('/users/{id}') #Done
def delete_user(id: str):
    result = db.user.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    
    return {"message": "usuario eliminado correctamente"}

# Auth
@user.post('/auth/login')
def login_user(email: str, password: str):
    user_data = db.user.find_one({"email": email, "password": password})
    if not user_data:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return userEntity(user_data)

@user.post('/auth/recover')
def recover_password(email: str):
    return email

@user.post('/auth/reset')
def reset_password(token: str, new_password: str):
    return {"token": token, "new_password": new_password}