def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "firstname": item.get("firstname"),
        "lastname": item.get("lastname"),
        "email": item.get("email"),
        "password": item.get("password"),
        "role": item.get("role"),
        "addresses": item.get("addresses", []),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt")
    }
