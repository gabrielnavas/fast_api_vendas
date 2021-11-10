from typing import List
from fastapi.responses import Response
from fastapi.routing import APIRouter
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from modules.shared.models import database
from modules.clients.models import Client
from modules.products.models import Product

from .models import Sale, SaleProduct

route = APIRouter()


class ProductBody(BaseModel):
    id: int
    amount: int


class SaleCreateBody(BaseModel):
    client_id: int
    products: List[ProductBody]
    total_price: float
    discount: float


@route.post("/sale", status_code=201, tags=["sale"])
def create(sale_body: SaleCreateBody, response: Response):
    try:
        with database.atomic() as transaction:  # Opens new transaction.
            try:
                sale = Sale.create(
                    total_price=sale_body.total_price,
                    discount=sale_body.discount,
                    client=Client.get(sale_body.client_id),
                )
                products_to_insert = [
                    {"product": p.id, "sale": sale.id}
                    for p in sale_body.products
                ]
                SaleProduct.insert_many(products_to_insert).execute()
                # for sale_product in sale_body.products:
                #     SaleProduct.create(
                #         product=Product.get(sale_product.id), sale=sale
                #     )
                return model_to_dict(sale)
            except Exception as ex:
                print(ex)
                transaction.rollback()

    except Exception as ex:
        print(ex)
        response.status_code = 500
