def userEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "firstname": item.get("firstname"),
        "lastname": item.get("lastname"),
        "email": item.get("email"),
        "password": item.get("password"),
        "role": item.get("role"),
        "createdAt": item.get("createdAt"),
        "updatedAt": item.get("updatedAt")
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
