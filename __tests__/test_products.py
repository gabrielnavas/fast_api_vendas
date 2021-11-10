import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import datetime

from modules.main import server
from modules.products.models import Product, ProductType

client = TestClient(server.app)


@pytest.fixture(autouse=True)
def run_around_tests():
    Product.delete().execute()
    ProductType.delete().execute()
    yield
    Product.delete().execute()
    ProductType.delete().execute()


def test_create_product():
    home = ProductType.create(name="Home")
    response = client.post(
        "/product",
        json={
            "name": "Apple",
            "amount": 44,
            "price": 22.11,
            "product_type_id": home.id,
        },
    )
    assert response.status_code == 201
    product = response.json()
    assert product["id"] > 0
    assert product["name"] == "Apple"
    assert product["amount"] == 44
    assert product["price"] == 22.11
    assert datetime.fromisoformat(product["created_at"])
    assert product["product_type"]["id"] == home.id
    assert product["product_type"]["name"] == home.name


def test_update_product():
    home = ProductType.create(name="Home")
    car = ProductType.create(name="Car")
    response = client.post(
        "/product",
        json={
            "name": "Apple",
            "amount": 44,
            "price": 22.11,
            "product_type_id": home.id,
        },
    )
    assert response.status_code == 201
    product = response.json()
    assert product["id"] > 0

    response = client.put(
        f"/product/{product['id']}",
        json={
            "name": "Apple",
            "amount": 22,
            "price": 55.22,
            "product_type_id": car.id,
        },
    )
    assert response.status_code == 204


def test_delete_product():
    home = ProductType.create(name="Home")
    response = client.post(
        "/product",
        json={
            "name": "Apple",
            "amount": 44,
            "price": 22.11,
            "product_type_id": home.id,
        },
    )
    assert response.status_code == 201
    product = response.json()
    assert product["id"] > 0

    # delete
    response = client.delete(
        f"/product/{product['id']}",
    )
    assert response.status_code == 204


def test_get_one_product():
    home = ProductType.create(name="Home")
    response = client.post(
        "/product",
        json={
            "name": "Apple",
            "amount": 44,
            "price": 22.11,
            "product_type_id": home.id,
        },
    )
    assert response.status_code == 201
    product = response.json()
    assert product["id"] > 0

    # get
    response = client.get(
        f"/product/{product['id']}",
    )
    assert response.status_code == 200
    product = response.json()

    assert product["id"] > 0
    assert product["name"] == "Apple"
    assert product["amount"] == 44
    assert product["price"] == 22.11
    assert datetime.fromisoformat(product["created_at"])
    assert product["product_type"]["id"] == home.id
    assert product["product_type"]["name"] == home.name


def test_get_one_all_products():
    len_products = 11
    products = []
    home = None
    for n in range(len_products):
        home = ProductType.create(name="Home" + str(n))
        response = client.post(
            f"/product",
            json={
                "name": "Apple",
                "amount": 44,
                "price": 22.11,
                "product_type_id": home.id,
            },
        )
        assert response.status_code == 201
        product = response.json()
        assert product["id"] > 0
        products.append(product)

    response = client.get(
        f"/product?name=Apple&amount=44&price=22.11&product_type_name={home.name}&offset=0&limit=9",
    )
    assert response.status_code == 200
    products_from_response = response.json()
    assert len(products_from_response) == 9
