from unittest import result
from config.db import db
from fastapi import APIRouter, HTTPException
from models.category import Category
from schemas.category import categoryEntity, categoriesEntity
from bson import ObjectId # type: ignore

category = APIRouter(prefix="/categories", tags=["Categories"])

# Create
@category.post('')
def create_category(category: Category): #Done
    if db.category.find_one({"name": category.name}):
        raise HTTPException(status_code=400, detail="El nombre de la categoria ya está registrado")
    else:
        new_category = dict(category)
        result = db.category.insert_one(new_category)
        created_category = db.category.find_one({"_id": result.inserted_id})
        db.categories.insert_one(created_category)
        return {"message": "Categoria creada correctamente"}


# Research
@category.get('')
def get_categories(): #Done
    return categoriesEntity(db.category.find())

@category.get('/{id}')
def get_categoryName_by_id(category_id: str):
    category_data = db.category.find_one({"_id": ObjectId(category_id)})
    if not category_data:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoryEntity(category_data)


# Update
@category.put('/{category_id}/name')
def update_category_name(category_id: str, name: str):
    return {"category_id": category_id, "name": name}
# Delete
@category.delete('/{category_id}')
def delete_category(category_id: str):  
    return category_id