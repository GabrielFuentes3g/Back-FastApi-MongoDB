from datetime import datetime
from fastapi import APIRouter, HTTPException

from models.product import Product
from config.db import db
from schemas.product import productEntity,productsEntity
from bson import ObjectId # type: ignore

product = APIRouter()

# Crate
@product.post('/products/')
def create_product(product: Product):
    new_product = dict(product)
    result = db.product.insert_one(new_product)
    created_product = db.product.find_one({"_id": result.inserted_id})
    return productEntity(created_product)

# Research
@product.get('/products/{id}')
def find_product(id: str):
    product_data = db.product.find_one({"_id": ObjectId(id)})
    if not product_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productEntity(product_data)

@product.get('/products')
def find_all_products():
    return productsEntity(db.product.find())

# Update
@product.put('/products/{id}')
def update_product(id: str, product: Product):
    updated_data = {**product.dict(), "updatedAt": datetime.utcnow()}
    result = db.product.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto actualizado correctamente"}

# Delete
@product.delete('/products/{id}')
def delete_product(id: str):
    result = db.product.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto eliminado correctamente"}