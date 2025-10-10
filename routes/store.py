from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.store import Store
from config.db import db
from schemas.store import storeEntity,storesEntity, storesFromUserEntity
from bson import ObjectId

store = APIRouter()


@store.post('/stores/')
def create_store(user_id: str, store_data: Store):
    try:
        new_store = store_data.dict()

        # Convertir logoURL a string si existe
        if new_store.get("logoURL"):
            new_store["logoURL"] = str(new_store["logoURL"])

        new_store["userID"] = user_id
        new_store["createdAt"] = datetime.utcnow()
        new_store["updatedAt"] = datetime.utcnow()
        result = db.store.insert_one(new_store)
        created_store = db.store.find_one({"_id": result.inserted_id})

        return storeEntity(created_store)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tienda: {str(e)}")







# Create

# Research
@store.get('/stores/{user_id}')
def find_all_stores_by_user(user_id: str):
    return storesFromUserEntity(user_id)

@store.get('/stores/{id}')
def find_store(id: str):
    store_data = db.store.find_one({"_id": ObjectId(id)})
    if not store_data:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return storeEntity(store_data)



@store.get('/stores')
def find_all_stores():
    return storesEntity(db.store.find())

# Update
@store.put('/stores/{id}')
def update_store(id: str, store: Store):
    updated_data = {**store.dict(), "updatedAt": datetime.utcnow()}
    result = db.store.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    return {"message": "tienda actualizado correctamente"}

# Delete
@store.delete('/stores/{id}')
def delete_store(id: str):
    result = db.store.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="tienda no encontrada")
    
    return {"message": "tienda eliminado correctamente"}