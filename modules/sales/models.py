from datetime import datetime

from modules.shared.models import Base, peewee
from modules.clients.models import Client
from modules.products.models import Product


class Sale(Base):
    total_price = peewee.DecimalField()
    discount = peewee.DecimalField()
    client = peewee.ForeignKeyField(Client)
    created_at = peewee.DateTimeField(default=datetime.utcnow)

    class Meta:
        table_name = "sale"
        schema = "sales"


class SaleProduct(Base):
    product = peewee.ForeignKeyField(Product)
    sale = peewee.ForeignKeyField(Sale)

    class Meta:
        primary_key = peewee.CompositeKey("product", "sale")
        table_name = "sale_product"
        schema = "sales"
