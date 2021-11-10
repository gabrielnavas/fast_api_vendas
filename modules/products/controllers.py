from typing import Optional
from fastapi.responses import Response
from fastapi.routing import APIRouter
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from datetime import datetime

from .models import Product, ProductType
from .usecases import ProductUsecase

route = APIRouter()


class ProductCreate(BaseModel):
    name: str
    amount: int
    price: float
    product_type_id: int


class ProductUpdate(BaseModel):
    name: str
    amount: int
    price: float
    product_type_id: int


product_usecase = ProductUsecase()


@route.post("/product", status_code=201, tags=["product"])
def create(product_create: ProductCreate, response: Response):
    try:
        product = product_usecase.store(
            name=product_create.name,
            amount=product_create.amount,
            price=product_create.price,
            product_type_id=product_create.product_type_id,
        )
        return model_to_dict(product)
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.put("/product/{id}", status_code=204, tags=["product"])
def update(id: int, product_update: ProductUpdate, response: Response):
    try:
        product = product_usecase.update(
            id=id,
            name=product_update.name,
            amount=product_update.amount,
            price=product_update.price,
            product_type_id=product_update.product_type_id,
        )
        if product is None:
            response.status_code = 404
            return
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.delete("/product/{id}", status_code=204, tags=["product"])
def delete(id: int, response: Response):
    try:
        if not product_usecase.delete(
            id=id,
        ):
            response.status_code = 404
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.get("/product/{id}", status_code=200, tags=["product"])
def get(id: int, response: Response):
    try:
        product = product_usecase.get(id)
        return model_to_dict(product)
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.get("/product", status_code=200, tags=["product"])
def get_all(
    response: Response,
    name: Optional[str] = None,
    amount: Optional[int] = None,
    price: Optional[float] = None,
    product_type_name: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
):
    try:
        query = {
            "name": name,
            "amount": amount,
            "price": price,
            "product_type_name": product_type_name,
        }
        products = product_usecase.get_all(
            query,
            offset,
            limit,
        )
        products = [model_to_dict(product) for product in products]
        return products
    except Exception as ex:
        print(ex)
        response.status_code = 500
