from typing import Optional, Dict, Any
from fastapi.responses import Response
from fastapi.routing import APIRouter
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict

from .usecases import ClientUseCase

route = APIRouter()
client_usecase = ClientUseCase()


class ClientCreate(BaseModel):
    name: str
    phone: str


class ClientUpdate(BaseModel):
    name: str
    phone: str


@route.post("/client", status_code=201, tags=["client"])
def create(client_create: ClientCreate, response: Response):
    try:
        client = client_usecase.store(
            name=client_create.name, phone=client_create.phone
        )
        return model_to_dict(client)
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.put("/client/{id}", status_code=200, tags=["client"])
def update(id: int, client_create: ClientUpdate, response: Response):
    try:
        client_updated = client_usecase.update(
            id=id, name=client_create.name, phone=client_create.phone
        )
        if client_updated is None:
            response.status_code = 404
            return
        return model_to_dict(client_updated)
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.delete("/client/{id}", status_code=204, tags=["client"])
def delete(id: int, response: Response):
    try:
        if not client_usecase.delete(id):
            response.status_code = 404
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.get("/client/{id}", status_code=200, tags=["client"])
def get(id: int, response: Response):
    try:
        client = client_usecase.get(id)
        if client is not None:
            return model_to_dict(client)
        else:
            response.status_code = 404
    except Exception as ex:
        print(ex)
        response.status_code = 500


@route.get(
    "/client",
    status_code=200,
    tags=["client"],
)
def get_all(
    response: Response,
    name: str = "",
    phone: str = "",
    offset: int = 0,
    limit: int = 10,
):
    try:
        products = client_usecase.get_all(
            {"name": name, "phone": phone}, offset, limit
        )
        data = [model_to_dict(p) for p in products]
        return data
    except Exception as ex:
        print(ex)
        response.status_code = 500
