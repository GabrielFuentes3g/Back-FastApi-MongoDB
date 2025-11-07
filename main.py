from fastapi import FastAPI

from routes.product import product
from routes.store import store
from routes.user import user
from routes.category import category
from routes.order import order
from routes.payment import payment

main = FastAPI()

main.include_router(product)
main.include_router(store)
main.include_router(payment)
main.include_router(order)
main.include_router(user)
main.include_router(category)
