from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.product import Product
from config.db import db
from schemas.product import productEntity,productsEntity
from bson import ObjectId # type: ignore

product = APIRouter(prefix="/products", tags=["Products"])

# Crate
@product.post('') 
def create_product(product: Product): #G
    new_product = dict(product)
    result = db.product.insert_one(new_product)
    created_product = db.product.find_one({"_id": result.inserted_id})
    return productEntity(created_product)

# Research
@product.get('/products/{id}')
def get_product_by_id(id: str): #G
    product_data = db.product.find_one({"_id": ObjectId(id)})
    if not product_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productEntity(product_data)

@product.get('')
def get_products():
    return productsEntity(db.product.find())

@product.get('/store/{store_id}')
def get_products_by_store(store_id: str):
    return store_id
    
@product.get('/category/{category_name}')
def get_products_by_category(category_name: str):
    return category_name


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

@product.put('/{product_id}/stock')
def update_product_stock(product_id: str, stockQuantity: int):
    return {"product_id": product_id, "stockQuantity": stockQuantity}

@product.put('/{product_id}/price')
def update_product_price(product_id: str, price: float):
    return {"product_id": product_id, "price": price}


# Delete
@product.delete('/products/{id}')
def delete_product(id: str):
    result = db.product.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto eliminado correctamente"}