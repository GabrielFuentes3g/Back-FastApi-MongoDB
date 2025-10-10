def storeEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "userID": item.get("userID"),
        "name": item.get("name"),
        "description": item.get("description"),
        "rating": item.get("rating"),
        "logoURL": item.get("logoURL"),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt")
    }

def storesEntity(entity) -> list:
    return [storeEntity(item) for item in entity]

def storesFromUserEntity(entity,user_id) -> list:
    filtered_stores = [item for item in entity if item.get("userID") == user_id]
    return [storeEntity(item) for item in filtered_stores]