import datetime
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


def shop_trip() -> None:
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
                shop_prices[shop.name] = round(customer.count_total_price(shop), 2)  # noqa: E501
                print(f"{customer.name}'s trip to the {shop.name} costs {shop_prices[shop.name]} dollars")  # noqa: E501
            chosen_shop = min(shop_prices, key=shop_prices.get)  # pyright: ignore # noqa: E501
            if customer.money < min(shop_prices.values()):
                print(f"{customer.name} doesn't have enough money to make a purchase in any shop")  # noqa: E501
                return
            shop_instance: Shop
            for shop in shops:
                if shop.name == chosen_shop:
                    shop_instance = shop
            print(f"{customer.name} rides to {chosen_shop}\n")
            curr_date = datetime.datetime.strftime(
                datetime.datetime.now(), "%d/%m/%y %H:%M:%S"
            )
            print(f"Date: {curr_date}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")
            for product, quantity in customer.product_cart.items():
                print(f"{quantity} {product}s for {quantity * shop_instance.products[product]}")  # pyright: ignore # noqa: E501
            print(f"See you again!\n{customer.name} rides home")
            print(f"{customer.name} now has {customer.money - shop_prices[shop_instance.name]}\n")  # pyright: ignore # noqa: E501
