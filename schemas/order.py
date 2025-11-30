def orderEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "userid": item.get("userid"),
        "orderDate": item.get("orderDate"),
        "status": item.get("status"),
        "totalAmount": item.get("totalAmount"),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt")
    }

def ordersEntity(entity) -> list:
    return [orderEntity(item) for item in entity]
