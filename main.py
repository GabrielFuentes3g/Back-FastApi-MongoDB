from fastapi import FastAPI

from routes.product import product
from routes.store import store
from routes.user import user
from routes.category import category

main = FastAPI()

main.include_router(product)
main.include_router(store)
main.include_router(user)
main.include_router(category)
