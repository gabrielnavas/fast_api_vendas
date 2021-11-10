from datetime import datetime

from modules.shared.models import Base, peewee


class Client(Base):
    name = peewee.CharField()
    phone = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.utcnow)
    updated_at = peewee.DateTimeField(null=True, default=None)

    class Meta:
        table_name = "client"
        schema = "clients"
