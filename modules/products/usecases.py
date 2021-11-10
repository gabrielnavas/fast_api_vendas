from typing import Dict, Any, List
from .models import Product, ProductType


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
        if len(query) > 0:
            products = (
                Product.select()
                .join(ProductType)
                .where(
                    (Product.name.contains(query.get("name", "")))
                    | (Product.amount == query.get("amount", ""))
                    | (Product.price == query.get("price", ""))
                    | (
                        ProductType.name.contains(
                            query.get("product_type_name", "")
                        )
                    )
                )
                .offset(offset)
                .limit(limit)
            )
            return products
        else:
            return Product.select().offset(offset).limit(limit)
