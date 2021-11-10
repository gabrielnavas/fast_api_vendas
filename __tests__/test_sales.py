import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime
import functools

from modules.main import server

from modules.products.models import Product, ProductType
from modules.clients.models import Client
from modules.sales.models import Sale, SaleProduct

client = TestClient(server.app)


@pytest.fixture(autouse=True)
def run_around_tests():
    SaleProduct.delete().execute()
    Sale.delete().execute()
    Product.delete().execute()
    ProductType.delete().execute()
    yield
    SaleProduct.delete().execute()
    Sale.delete().execute()
    Product.delete().execute()
    ProductType.delete().execute()


def test_create_product():
    # create client
    response_client = client.post(
        "/client",
        json={
            "name": "Gabriel",
            "phone": "18997865522",
        },
    )
    client_result = response_client.json()

    # create products
    products = []
    for index, product in enumerate(range(20)):
        home = ProductType.create(name="home" + str(index))
        response_product = client.post(
            "/product",
            json={
                "name": "Apple" + str(index),
                "amount": 44 + index,
                "price": 22.11 + index * 2,
                "product_type_id": home.id,
            },
        )
        products.append(response_product.json())
    total_price = 0
    for product in products:
        total_price += product["amount"] * product["price"]

    products_wrapper_to_post = []
    for index, product in enumerate(products):
        products_wrapper_to_post.append(
            {"id": product["id"], "amount": product["amount"]}
        )

    # create sale
    discount = 0.10
    response = client.post(
        "/sale",
        json={
            "client_id": client_result["id"],
            "products": products_wrapper_to_post,
            "total_price": total_price,
            "discount": discount,
        },
    )
    assert response.status_code == 201
    sale = response.json()
    assert sale["id"] > 0
    assert sale["total_price"] == total_price
    assert sale["discount"] == discount
    assert sale["created_at"]
    assert sale["client"]["id"]
