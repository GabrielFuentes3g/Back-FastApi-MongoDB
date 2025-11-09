from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
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
    
@product.get('/category/{categoryId}') 
def get_products_by_categoryId(categoryId: str): #Done
    if len(categoryId) != 24:
        raise HTTPException(status_code=404, detail="Categoría no encontrada, formato no valido")
    category_data = db.category.find_one({"_id": ObjectId(categoryId)})
    if not category_data:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    products = db.product.find({"categoriesId": categoryId})
    return productsEntity(products)
    


# Update
@product.put('/{product_id}/image')
def update_product_image(product_id: str, image_url: str):
    if not image_url.startswith("http") or not image_url.endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(status_code=400, detail="URL de imagen no válida")
    if len(product_id) != 24:
        raise HTTPException(status_code=400, detail="ID de producto inválido")
    product_data = db.product.find_one({"_id": ObjectId(product_id)})
    if not product_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    result = db.product.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"imageURL": image_url, "updatedAt": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Imagen del producto actualizada correctamente"}


@product.put('/{product_id}/name')
def update_product_name(product_id: str, name: str): #Done
    product = db.product.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if db.product.find_one({"name": name, "storeId": product["storeId"]}):
        raise HTTPException(status_code=400, detail="El nombre del producto ya está registrado en esta tienda")
    db.product.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "name": name,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    return {"message": "Nombre del producto actualizado correctamente"}

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
def update_product_description(product_id: str, description: str): #Done
    if len(product_id) != 24:
        raise HTTPException(status_code=404, detail="Producto no encontrado, formato no valido")
    product = db.product.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.product.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "description": description,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    return {"message": "Descripción del producto actualizada correctamente"}

@product.put('/{product_id}/stock')
def update_product_stock(product_id: str, stockQuantity: int): #Done
    #el valor no puede ser negativo
    if stockQuantity < 0:
        raise HTTPException(status_code=400, detail="La cantidad de stock no puede ser negativa")
    if len(product_id) != 24:
        raise HTTPException(status_code=404, detail="Producto no encontrado, formato no valido")
    product = db.product.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.product.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "stockQuantity": stockQuantity,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    return {"message": "Cantidad de stock del producto actualizada correctamente"}

@product.put('/{product_id}/price')
def update_product_price(product_id: str, price: float): #Done
    if price < 0:
        raise HTTPException(status_code=400, detail="El precio no puede ser negativo")
    if len(product_id) != 24:
        raise HTTPException(status_code=404, detail="Producto no encontrado, formato no valido")
    product = db.product.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.product.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "price": price,
                "updatedAt": datetime.utcnow()
            }
        }
    )
    return {"message": "Precio del producto actualizado correctamente"}

# Delete
@product.delete('/products/{id}')
def delete_product(id: str): #Done
    if len(id) != 24:
        raise HTTPException(status_code=400, detail="ID de producto invalido")
    result = db.product.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto eliminado correctamente"}

@product.delete('/products/{id}/categories/{categoryId}')
def delete_category_from_product(id: str,categoryId: str): #Done
    if len(id) != 24:
        raise HTTPException(status_code=400, detail="ID de producto invalido")
    if len(categoryId) != 24:
        raise HTTPException(status_code=400, detail="ID de categoría invalido")
    product = db.product.find_one({"_id": ObjectId(id)})
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    category = db.category.find_one({"_id": ObjectId(categoryId)})
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoryId not in product.get("categoriesId", []):
        raise HTTPException(status_code=400, detail="La categoría no está asignada a este producto")
    db.product.update_one(
        {"_id": ObjectId(id)},
        {
            "$pull": {"categoriesId": categoryId},
            "$set": {"updatedAt": datetime.utcnow()}
        }
    )
    return {"message": "Categoría eliminada correctamente del producto"}