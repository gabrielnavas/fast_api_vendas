from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.shared.models import database

# create table
from modules.products.models import Product, ProductType
from modules.clients.models import Client
from modules.sales.models import Sale, SaleProduct

# routes
from modules.products.controllers import route as route_products
from modules.clients.controllers import route as route_clients
from modules.sales.controllers import route as route_sales

app = FastAPI()
app.include_router(route_products)
app.include_router(route_clients)
app.include_router(route_sales)


@app.on_event("startup")
async def startup_event():
    # cors
    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # database
    with database:
        database.create_tables(
            [Product, ProductType, Client, Sale, SaleProduct]
        )

    # add initial data
    # TODO NEED TO REFACTORY THIS
    for name in ["Home", "Car", "Eletronic"]:
        if ProductType.select().where(ProductType.name == name).count() == 0:
            ProductType.create(name=name)

    ProductType.get(name="Car")
    ProductType.get(name="Eletronic")


@app.get("/")
async def root():
    return {"server online": True}
