from markets.crypto_market import BitRexMarket, BitBayMarket
from markets.normal_currency_market import *
from markets.stock_markets import *


def get_crypto_currencies(wallet):
    return get_currencies_pairs(wallet.get_crypto_currencies())


def get_normal_currencies(wallet):
    return get_currencies_pairs(wallet.get_normal_currencies())


def get_foreign_stocks(wallet):
    return get_stocks(wallet.get_foreign_stock())


def get_polish_stocks(wallet):
    return get_stocks(wallet.get_polish_stocks())


def get_stocks(stocks):
    return [(stock["name"], stock["quote_currency"]) for stock in stocks]


def get_currencies_pairs(currency_resources):
    return [(resource["base_currency"], resource["quote_currency"]) for resource in currency_resources]


def get_crypto_markets(resources):
    return [BitRexMarket(resources), BitBayMarket(resources)]


def get_normal_markets(resources):
    return [ExchangeRates(resources), NBP(resources)]


def get_foreign_markets(resources):
    return [AlphaVantageMarket(resources), TwelveDataMarket(resources)]


def get_polish_markets(resources):
    return [PolishMarket(WSE_NAME, resources)]


def get_transaction_result(transaction_manager):
    user_resources = transaction_manager.get_best_prices_for_owned_resources(1.0)
    ten_percent_prices = transaction_manager.get_best_prices_for_owned_resources(0.1)

    transaction_result = [(user_resources[i][0], user_resources[i][1], ten_percent_prices[i][1], user_resources[i][2])
                          for i in range(len(user_resources))]

    return transaction_result


def display_user_resources(user_resources):
    title = "{:<25} {:<25} {:<20} {:<25} {:<25} {:<25} {:<25} {:<26} {:<26} {:<25} {:<25}"
    print(title.format("Resource Name", "Resource Type", "Best Place", "Buy Price Per Unit", "Buy Volume", "Buy Price",
                       "Best Sell Price", "Ten Percent Sell Price", "Gain", "Ten Percent Gain", "Currency"))

    total_sell_price = 0
    total_ten_percent_price = 0
    total_net_gain = 0
    total_ten_percent_gain = 0

    exchange_resources = []
    for resource in user_resources:
        exchange_resources.append((resource[0]["quote_currency"], BASE_CURRENCY))

    exchange_center = NBP(exchange_resources)

    for index, resource in enumerate(user_resources):
        resource_name = resource[0]["name"]
        resource_type = resource[0]["type"]
        resource_market_name = resource[3]
        resource_bought_price_per_unit = resource[0]["price_per_unit"] * exchange_center.get_exchange_rates()[index]["exchange_rate"]

        resource_bought_volume = resource[0]["quantity"]
        resource_bought_price = resource_bought_price_per_unit * resource_bought_volume
        resource_best_sell_price = resource[1] * exchange_center.get_exchange_rates()[index]["exchange_rate"]
        resource_ten_percent_sell_price = resource[2] * exchange_center.get_exchange_rates()[index]["exchange_rate"]

        resource_gain = resource_best_sell_price - resource_bought_price
        resource_gain = resource_gain if resource_gain < 0 else resource_gain * (1 - POLISH_TAX)

        resource_ten_percent_gain = resource_ten_percent_sell_price - resource_bought_price * 0.1
        resource_ten_percent_gain = resource_ten_percent_gain if resource_ten_percent_gain < 0 else \
            resource_ten_percent_gain * (1 - POLISH_TAX)

        resource_currency = BASE_CURRENCY

        total_sell_price += resource_best_sell_price
        total_ten_percent_price += resource_ten_percent_sell_price
        total_net_gain += resource_gain
        total_ten_percent_gain += resource_ten_percent_gain

        inner_text = "{:<25} {:<25} {:<6} {:>25.5f} {:>25.5f}  {:>25.5f} {:>25.5f} {:>25.5f} {:>25.5f} {:>25.5f} {:>18}"

        print(inner_text.format(resource_name, resource_type, resource_market_name, resource_bought_price_per_unit,
                                resource_bought_volume, resource_bought_price, resource_best_sell_price,
                                resource_ten_percent_sell_price, resource_gain, resource_ten_percent_gain,
                                resource_currency))

    total_text = "TOTAL: {:>140} {:>15.5f} {:>9} {:>15.5f} {:>9} {:>15.5f} {:>9} {:>15.5f} {:>14} {:<10}"

    print(total_text.format("", total_sell_price, "", total_ten_percent_price, "", total_net_gain, "",
          total_ten_percent_gain, "", BASE_CURRENCY))


def display_arbitration_result(arbitration_result):
    title = "\n\n\n{:<25} {:<25} {:<25} {:<25} {:<25} {:<27} {:<25}"
    print(title.format("Resource Name", "Direction", "Ask Price", "Bid Price", "Gain", "Percent Gain", "Currency"))

    exchange_resources = []
    for currency in arbitration_result:
        if currency["Name"] != "ERROR-ERROR":
            exchange_resources.append((currency["Name"].split("-")[1], BASE_CURRENCY))
        else:
            exchange_resources.append((BASE_CURRENCY, BASE_CURRENCY))

    total_ask_price = 0
    total_bid_price = 0
    total_gain = 0
    exchange_center = NBP(exchange_resources)

    for index, result in enumerate(arbitration_result):
        resource_name = result["Name"]
        resource_direction = result["Direction"]
        resource_ask_price = result["Ask Price"] * exchange_center.get_exchange_rates()[index]["exchange_rate"]
        resource_bid_price = result["Bid Price"] * exchange_center.get_exchange_rates()[index]["exchange_rate"]
        resource_gain = result["Gain"] * exchange_center.get_exchange_rates()[index]["exchange_rate"]
        resource_percent_gain = result["Percent Gain"]

        total_ask_price += resource_ask_price
        total_bid_price += resource_bid_price
        total_gain += resource_gain

        inner_text = "{:<25} {:<11} {:>25.5f} {:>25.5f} {:>25.5f} {:>25.5f}% {:>18}"

        print(inner_text.format(resource_name, resource_direction, resource_ask_price, resource_bid_price,
                                resource_gain, resource_percent_gain, BASE_CURRENCY))

    print("Total {:>41} {:>15.5f} {:>9} {:>15.5f} {:>9} {:>15.5f} {:>34} {:>10}".
          format("", total_ask_price, "", total_bid_price, "", total_gain, "", BASE_CURRENCY))
