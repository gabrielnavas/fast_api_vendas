from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from modules.clients import models
from modules.main import server

client = TestClient(server.app)


@pytest.fixture(autouse=True)
def run_around_tests():
    models.Client.delete().execute()
    yield
    models.Client.delete().execute()


def test_create_product():
    response = client.post(
        "/client",
        json={
            "name": "Gabriel",
            "phone": "18997865522",
        },
    )
    assert response.status_code == 201
    client_result = response.json()
    assert client_result["id"] > 0
    assert client_result["name"] == "Gabriel"
    assert client_result["phone"] == "18997865522"
    assert datetime.fromisoformat(client_result["created_at"])


def test_update_product():
    # create client
    response = client.post(
        "/client",
        json={
            "name": "Gabriel",
            "phone": "18997865522",
        },
    )
    assert response.status_code == 201
    client_result = response.json()
    id = client_result["id"]
    assert id > 0

    # update
    response = client.put(
        f"/client/{id}",
        json={
            "name": "Joel",
            "phone": "18997865522",
        },
    )
    assert response.status_code == 200
    client_result = response.json()
    assert client_result["id"] == id
    assert client_result["name"] == "Joel"
    assert client_result["phone"] == "18997865522"
    assert datetime.fromisoformat(client_result["created_at"])
    assert datetime.fromisoformat(client_result["updated_at"])


def test_delete_product():
    # create client
    response = client.post(
        "/client",
        json={
            "name": "Gabriel",
            "phone": "18997865522",
        },
    )
    assert response.status_code == 201
    client_result = response.json()
    id = client_result["id"]
    assert id > 0

    # delete
    response = client.delete(
        f"/client/{id}",
    )
    assert response.status_code == 204


def test_get_one_product():
    # create client
    response = client.post(
        "/client",
        json={
            "name": "Gabriel",
            "phone": "18997865522",
        },
    )
    assert response.status_code == 201
    client_result = response.json()
    id = client_result["id"]
    assert id > 0

    # get
    response = client.get(
        f"/client/{id}",
    )
    assert response.status_code == 200
    client_result = response.json()
    assert client_result["id"] > 0
    assert client_result["name"] == "Gabriel"
    assert client_result["phone"] == "18997865522"
    assert datetime.fromisoformat(client_result["created_at"])


def test_get_all_products():
    # create client
    len_product = 11
    products = []
    name_test = "Gabriel"
    phone_test = "18997865522"

    for product in range(len_product):
        response = client.post(
            "/client",
            json={
                "name": name_test,
                "phone": phone_test,
            },
        )
        assert response.status_code == 201
        client_result = response.json()
        products.append(client_result)
        assert client_result["id"] > 0

    # get all
    response = client.get(
        f"/client?name={name_test[0:2]}&phone={phone_test[0:3]}&offset=1&limit=9",
    )
    assert response.status_code == 200
    client_result = response.json()
    assert len(client_result) == 9
