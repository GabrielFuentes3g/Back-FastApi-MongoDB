def orderItemEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "orderId": item.get("orderId"),
        "productId": item.get("productId"),
        "name": item.get("name"),
        "price": item.get("price"),
        "quantity": item.get("quantity"),
        "subtotal": item.get("subtotal"),
    }
def orderItemsEntity(entity) -> list:
    return [orderItemEntity(item) for item in entity]