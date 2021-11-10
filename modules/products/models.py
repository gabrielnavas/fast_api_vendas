from datetime import datetime

from modules.shared.models import Base, peewee


class ProductType(Base):
    name = peewee.CharField()

    class Meta:
        table_name = "product_type"
        schema = "products"


class Product(Base):
    name = peewee.CharField()
    amount = peewee.IntegerField()
    price = peewee.DecimalField()
    created_at = peewee.DateTimeField(default=datetime.utcnow)
    product_type = peewee.ForeignKeyField(ProductType)

    class Meta:
        table_name = "product"
        schema = "products"
