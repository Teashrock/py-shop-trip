from dataclasses import dataclass

try:
    from app.car import Car
    from app.shop import Shop
except ImportError:
    from car import Car
    from shop import Shop


@dataclass
class Customer:
    name: str
    product_cart: dict[str, int]
    location: list[int]
    money: int
    car: Car

    def count_total_price(self, shop: Shop):
        result = 0
        for product in self.product_cart:
            result += self.product_cart[product] * shop.products[product]
        result += self.car.full_price
        return result
