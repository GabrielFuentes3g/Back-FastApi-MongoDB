def categoryEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item.get("name")
    }

def categoriesEntity(entity) -> list:
    return [categoryEntity(item) for item in entity]