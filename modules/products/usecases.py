import functools
from typing import Dict, Any, List
from .models import Product, ProductType
import functools
import operator


class ProductUsecase:
    def store(
        self, name: str, amount: int, price: float, product_type_id: int
    ) -> Product:
        return Product.create(
            name=name,
            amount=amount,
            price=price,
            product_type=product_type_id,
        )

    def update(
        self,
        id: int,
        name: str,
        amount: int,
        price: float,
        product_type_id: int,
    ) -> bool:
        product = Product.get_or_none(id)
        if product is None:
            return False
        product.name = name
        product.amount = amount
        product.price = price
        product.product_type = ProductType.get(product_type_id)
        product.save()
        return True

    def delete(self, id: int) -> bool:
        product = Product.get_or_none(id)
        if product is None:
            return False
        rows_count = product.delete_instance()
        return rows_count > 0

    def get(self, id: int) -> Product:
        return Product.get_or_none(id)

    def get_all(
        self, query: Dict[str, Any], offset=0, limit=10
    ) -> List[Product]:
        query_list = [
            Product.name.contains(query["name"])
            if query["name"] is not None and len(query["name"]) > 0
            else None,
            Product.price == query["amount"]
            if query["amount"] is not None and query["amount"] > 0
            else None,
            Product.price == query["price"]
            if query["price"] is not None and query["price"] > 0
            else None,
            ProductType.name.contains(query["product_type_name"])
            if query["product_type_name"] is not None
            and len(query["product_type_name"]) > 0
            else None,
        ]
        query_list_remove_none = list(
            filter(lambda query: query is not None, query_list)
        )

        if len(query_list_remove_none) > 0:
            query_or_operator = functools.reduce(
                operator.or_, query_list_remove_none
            )
            return (
                Product.select()
                .join(ProductType)
                .where(query_or_operator)
                .offset(offset)
                .limit(limit)
            )
        else:
            return (
                Product.select().join(ProductType).offset(offset).limit(limit)
            )

    def get_all_products_type(self) -> List[Product]:
        return ProductType.select()
