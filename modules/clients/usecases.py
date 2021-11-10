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

        if limit == 0:
            clients = (
                Client.select()
                .where(
                    (Client.name.contains(query.get("name", "")))
                    | (Client.phone.contains(query.get("phone", "")))
                )
                .offset(offset)
            )
            return clients

        if len(query) > 0:
            clients = (
                Client.select()
                .where(
                    (Client.name.contains(query.get("name", "")))
                    | (Client.phone.contains(query.get("phone", "")))
                )
                .offset(offset)
                .limit(limit)
            )
            return clients

        clients = Client.select().offset(offset).limit(limit)
        return clients
