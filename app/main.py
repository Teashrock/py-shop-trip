import json
import os


try:
    from app.car import Car
    from app.customer import Customer
    from app.shop import Shop
except ImportError:
    from car import Car
    from customer import Customer
    from shop import Shop


def shop_trip():
    with open(os.path.join("app", "config.json"), "r") as la_json:
        json_content = json.load(la_json)
        fuel_price = json_content["FUEL_PRICE"]
        customers: list[Customer] = []
        shops: list[Shop] = []
        for customer_data in json_content["customers"]:
            customers.append(
                Customer(
                    customer_data["name"],
                    customer_data["product_cart"],
                    customer_data["location"],
                    customer_data["money"],
                    Car(
                        customer_data["car"]["brand"],
                        fuel_price,
                        customer_data["car"]["fuel_consumption"]
                    )
                )
            )
        for shop_data in json_content["shops"]:
            shops.append(
                Shop(
                    shop_data["name"],
                    shop_data["location"],
                    shop_data["products"]
                )
            )
        for customer in customers:
            print(f"{customer.name} has {customer.money} dollars")
            shop_prices = {}
            for shop in shops:
                shop_prices[shop.name] = customer.count_total_price(shop)
                print(f"{customer.name}'s trip to the {shop.name} costs {shop_prices[shop.name]} dollars")
            chosen_shop = min(shop_prices, key=shop_prices.get)  # pyright: ignore
            print(f"{customer.name} rides to {chosen_shop}")
