def productEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "storeId": item.get("storeId"),
        "name": item.get("name"),
        "description": item.get("description"),
        "price": item.get("price"),
        "stockQuantity": item.get("stockQuantity"),
        "categoriesId": item.get("categoriesId", []),
        "imageURL": item.get("imageURL"),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt")
    }

def productsEntity(entity) -> list:
    return [productEntity(item) for item in entity]