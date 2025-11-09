from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.store import Store
from config.db import db
from schemas.store import storeEntity,storesEntity, storesFromUserEntity
from bson import ObjectId # type: ignore

store = APIRouter(prefix="/stores", tags=["Stores"])

# Create
@store.post('')
def create_store(user_id: str, store_data: Store): #Done
    try:
        new_store = store_data.dict()
        # Convertir logoURL a string si existe
        if new_store.get("logoURL"):
            new_store["logoURL"] = str(new_store["logoURL"])
        # validar si el nombre de la tienda ya existe
        if db.store.find_one({"name": new_store["name"]}):
            raise HTTPException(status_code=400, detail="El nombre de la tienda ya está registrado")
        else:
            new_store["userID"] = user_id
            new_store["createdAt"] = datetime.utcnow()
            new_store["updatedAt"] = datetime.utcnow()
            result = db.store.insert_one(new_store)
            created_store = db.store.find_one({"_id": result.inserted_id})

        return storeEntity(created_store)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tienda: {str(e)}")

# Research
@store.get('')
def get_stores(): #Done
    return storesEntity(db.store.find())

@store.get('/user/{user_id}')
def get_stores_by_user(user_id: str): #Done
    stores = db.store.find({"userID": user_id})
    return storesFromUserEntity(stores, user_id)


@store.get('/{store_id}')
def get_store_by_id(store_id: str): #Done
    store_data = db.store.find_one({"_id": ObjectId(store_id)})
    if not store_data:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return storeEntity(store_data)


# Update

@store.put('/{store_id}/description') #Done
def update_store_description(store_id: str, store: dict):
    updated_data = {k: v for k, v in store.items() if k in ["description"]}
    if not updated_data:
        raise HTTPException(status_code=400, detail="No hay datos válidos para actualizar")
    
    updated_data["updatedAt"] = datetime.utcnow()
    
    result = db.store.update_one(
        {"_id": ObjectId(store_id)},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return {"message": "descripción de la tienda actualizada correctamente"}


@store.put('/{store_id}/logo')
def update_store_logo(store_id: str, logo_url: str): #Done
    if not logo_url.startswith("http") or not logo_url.endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(status_code=400, detail="URL de logo no válida")
    result = db.store.update_one(
        {"_id": ObjectId(store_id)},
        {"$set": {"logoURL": logo_url, "updatedAt": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return {"message": "logo de la tienda actualizado correctamente"}

@store.put('/{store_id}/rating')
def update_store_rating(store_id: str, rating: float): #Done
    if rating < 0 or rating > 5:
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 0 y 5")
    
    result = db.store.update_one(
        {"_id": ObjectId(store_id)},
        {"$set": {"rating": rating, "updatedAt": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return {"message": "calificación de la tienda actualizada correctamente"}

# Delete
@store.delete('/{store_id}') #Done
def delete_store(store_id: str):
    result = db.store.delete_one({"_id": ObjectId(store_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    
    return {"message": "tienda eliminado correctamente"}