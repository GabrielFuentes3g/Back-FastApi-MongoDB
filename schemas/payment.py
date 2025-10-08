def paymentEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "orderid": item.get("orderid"),
        "paymentMethod": item.get("paymentMethod"),
        "paymentDate": item.get("paymentDate"),
        "amount": item.get("amount"),
        "status": item.get("status")
    }

def paymentsEntity(entity) -> list:
    return [paymentEntity(item) for item in entity]
