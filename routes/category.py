from config.db import db
from fastapi import APIRouter
from models.category import Category
from schemas.category import categoryEntity, categoriesEntity

category = APIRouter(prefix="/categories", tags=["Categories"])

# Create
@category.post('')
def create_product(category: Category):
    return category

# Research
@category.get('')
def get_categories():
    return ""

@category.get('/{id}')
def get_category_by_id(category_id: str):
    return category_id

@category.get('/name/{category_name}')
def get_categories_by_name(category_name: str):
    return category_name

# Update
@category.put('/{category_id}/name')
def update_category_name(category_id: str, name: str):
    return {"category_id": category_id, "name": name}
# Delete
@category.delete('/{category_id}')
def delete_category(category_id: str):  
    return category_id