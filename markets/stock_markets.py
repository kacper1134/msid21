import requests
import json
import quandl
import quandl.errors.quandl_error
from configuration.settings import *


class AlphaVantageMarket:
    def __init__(self, stocks):
        self.name = MARKET_ALPHA_VANTAGE["name"]
        self.stocks = self.get_resources(stocks)

    def get_resources(self, stocks):
        resources = []

        for stock in stocks:
            data = self.__load_data(MARKET_ALPHA_VANTAGE["url"], stock[0])
            data = data if "Global Quote" in data.keys() else {"Global Quote": {}}
            price = float(data["Global Quote"]["05. price"]) if "05. price" in data["Global Quote"].keys() else 0.0

            resources.append({"stock_name": stock[0], "price": price})

        return resources

    def __load_data(self, url, stock_symbol):
        try:
            headers = {
                "x-rapidapi-key": self.get_access_key(),
                "x-rapidapi-host": MARKET_ALPHA_VANTAGE["host"]
            }
            querystring = {"function": "GLOBAL_QUOTE", "symbol": stock_symbol}
            res = requests.request("GET", url, headers=headers, params=querystring)

            return json.loads(res.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException, requests.exceptions.Timeout):
            return {}

    def get_access_key(self):
        access_key = 0
        try:
            with open(MARKET_ALPHA_VANTAGE["access_key_path"]) as f:
                if f:
                    access_key = f.read()
        except FileNotFoundError:
            pass

        return access_key

    def get_stocks(self):
        return self.stocks

    def display_stocks(self):
        for stock in self.stocks:
            print(stock)


class TwelveDataMarket:
    def __init__(self, stocks):
        self.name = MARKET_TWELVE_DATA["name"]
        self.stocks = self.get_resources(stocks)

    def get_resources(self, stocks):
        resources = []

        for stock in stocks:
            data = self.__load_data(MARKET_TWELVE_DATA["url"], stock[0])

            price = float(data["price"]) if "price" in data.keys() else 0.0

            resources.append({"stock_name": stock[0], "price": price})

        return resources

    def __load_data(self, url, stock_symbol):
        try:
            headers = {
                "x-rapidapi-key": self.get_access_key(),
                "x-rapidapi-host": MARKET_TWELVE_DATA["host"]
            }
            querystring = {"function": "GLOBAL_QUOTE", "symbol": stock_symbol}
            res = requests.request("GET", url, headers=headers, params=querystring)

            return json.loads(res.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException, requests.exceptions.Timeout):
            return {}

    def get_access_key(self):
        access_key = 0
        try:
            with open(MARKET_TWELVE_DATA["access_key_path"]) as f:
                if f:
                    access_key = f.read()
        except FileNotFoundError:
            pass

        return access_key

    def get_stocks(self):
        return self.stocks

    def display_stocks(self):
        for stock in self.stocks:
            print(stock)


class PolishMarket:
    def __init__(self, name, stocks):
        self.name = name
        quandl.ApiConfig.api_key = self.get_access_key()
        self.stocks = self.get_resources(stocks)

    def get_resources(self, stocks):
        resources = []

        for stock in stocks:
            stock_name = stock[0]
            data = {}

            try:
                data = quandl.get(self.name + "/" + stock_name)
            except quandl.errors.quandl_error.NotFoundError:
                pass

            price = data["Close"][-1] if "Close" in data.keys() else 0.0

            resources.append({"stock_name": stock[0], "price": price})

        return resources

    def get_stocks(self):
        return self.stocks

    def display_stocks(self):
        for stock in self.stocks:
            print(stock)

    def get_access_key(self):
        access_key = 0
        try:
            with open(QUANDL_API_KEY_FILE) as f:
                if f:
                    access_key = f.read()
        except FileNotFoundError:
            pass
        return access_key
