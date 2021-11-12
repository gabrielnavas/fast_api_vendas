import functools
import operator
from typing import List, Dict, Any, Union
from datetime import datetime


from .models import Client


class ClientUseCase:
    def store(self, name: str, phone: str) -> Client:
        return Client.create(
            name=name,
            phone=phone,
        )

    def update(self, id: int, name: str, phone: str) -> Client:
        client = Client.get_or_none(id=id)
        if client is None:
            return None
        client.name = name
        client.phone = phone
        client.updated_at = datetime.utcnow()
        client.save()
        return client

    def delete(self, id: int) -> bool:
        client = Client.get_or_none(id=id)
        if client is None:
            return False
        rows_count = client.delete_instance()
        return rows_count > 0

    def get(self, id: int) -> Union[Client, None]:
        return Client.get_or_none(id=id)

    def get_all(
        self, query: Dict[str, Any], offset=0, limit=10
    ) -> List[Client]:
        # set None if no query params
        query_list = [
            Client.name.contains(query["name"])
            if query["name"] is not None and len(query["name"]) > 0
            else None,
            Client.phone.contains(query["phone"])
            if query["phone"] is not None and len(query["phone"]) > 0
            else None,
        ]
        # remove nones
        query_list_remove_none = list(
            filter(lambda query: query is not None, query_list)
        )

        if len(query_list_remove_none) > 0:
            query_or_operator = functools.reduce(
                operator.or_, query_list_remove_none
            )
            return (
                Client.select()
                .where(query_or_operator)
                .offset(offset)
                .limit(limit)
            )
        return Client.select().offset(offset).limit(limit)
