from fastapi import FastAPI

from routes.product import product

main = FastAPI()

main.include_router(product)