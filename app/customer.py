from dataclasses import dataclass
from math import sqrt

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

    def count_total_price(self, shop: Shop) -> float:
        result = 0
        for product in self.product_cart:
            result += self.product_cart[product] * shop.products[product]
        # Calculating distance
        # √((x₂ - x₁)² + (y₂ - y₁)²)
        distance = sqrt((shop.location[0] - self.location[0]) ** 2 + (shop.location[1] - self.location[1]) ** 2)
        result += self.car.full_price * distance * 2
        return result
