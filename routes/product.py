from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.product import Product
from config.db import db
from schemas.product import productEntity,productsEntity
from bson import ObjectId # type: ignore

product = APIRouter(prefix="/products", tags=["Products"])

# Create
@product.post('') 
def create_product(store_id: str, product: Product): #Done
    if len(store_id) != 24:
        raise HTTPException(status_code=404, detail="Tienda no encontrada, formato no valido")    
    new_product = product.dict()
    
    store_data = db.store.find_one({"_id": ObjectId(store_id)})
    if not store_data:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    
    if db.product.find_one({"name": new_product["name"], "storeId": store_id}):
        raise HTTPException(status_code=400, detail="El nombre del producto ya está registrado en esta tienda")
    
    new_product["storeId"] = store_id
    new_product["createdAt"] = datetime.utcnow()
    new_product["updatedAt"] = datetime.utcnow()
    
    result = db.product.insert_one(new_product)
    created_product = db.product.find_one({"_id": result.inserted_id})
    return productEntity(created_product)

# Research
@product.get('/products/{id}')
def get_product_by_id(id: str): #Done
    product_data = db.product.find_one({"_id": ObjectId(id)})
    if not product_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productEntity(product_data)

@product.get('')
def get_products(): #Done
    return productsEntity(db.product.find())

@product.get('/store/{store_id}') 
def get_products_by_store(store_id: str): #Done
    if len(store_id) != 24:
        raise HTTPException(status_code=404, detail="Tienda no encontrada, formato no valido")
    products = db.product.find({"storeId": store_id})
    return productsEntity(products)
    
@product.get('/category/{category_name}') 
def get_products_by_category(category_name: str):
    return category_name


# Update

@product.put('/{product_id}/name')
def update_product_name(product_id: str, name: str):
    return {"product_id": product_id, "name": name}

@product.put('/products/{id}')
def update_product_category(id: str,categoryId: str, product: Product): #Done
    product = db.product.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    category = db.category.find_one({"_id": ObjectId(categoryId)})
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoryId in product.get("categoriesId", []):
        raise HTTPException(status_code=400, detail="La categoría ya está asignada a este producto")
    db.product.update_one(
        {"_id": ObjectId(id)},
        {
            "$push": {"categoriesId": categoryId},
            "$set": {"updatedAt": datetime.utcnow()}
        }
    )
    return {"message": "Categoría añadida correctamente al producto"}

@product.put('/{product_id}/description')
def update_product_description(product_id: str, description: str):
    return {"product_id": product_id, "description": description}

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