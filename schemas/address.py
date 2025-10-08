def addressEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "userid": item.get("userid"),
        "street": item.get("street"),
        "city": item.get("city"),
        "state": item.get("state"),
        "postalCode": item.get("postalCode"),
        "country": item.get("country")
    }

def addressesEntity(entity) -> list:
    return [addressEntity(item) for item in entity]
