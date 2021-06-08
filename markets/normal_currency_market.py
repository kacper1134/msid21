from configuration.settings import *
import requests
import json


class ExchangeRates:
    def __init__(self, currencies):
        self.name = MARKET_EXCHANGE_RATE["name"]
        self.currencies = currencies
        self.resources = self.__load_resources()

    def __load_resources(self):
        resources = []

        access_key = self.get_access_key()

        currency_info = ExchangeRates.__load_data(MARKET_EXCHANGE_RATE["url"].format(access_key))

        currency_info = currency_info if "rates" in currency_info.keys() else {"rates": {}}

        for currency in self.currencies:
            base_currency_value = 1.0
            quote_currency_value = 1.0

            if currency[0] != MARKET_EXCHANGE_RATE["base_currency"]:
                if currency[0] not in currency_info["rates"].keys():
                    currency_info["rates"][currency[0]] = 1.0

                base_currency_value *= currency_info["rates"][currency[0]]

            if currency[1] != MARKET_EXCHANGE_RATE["base_currency"]:
                if currency[1] not in currency_info["rates"].keys():
                    currency_info["rates"][currency[1]] = 0.0

                quote_currency_value *= currency_info["rates"][currency[1]]

            resources.append({"currencies": currency, "exchange_rate": quote_currency_value / base_currency_value})

        return resources

    @staticmethod
    def __load_data(url):
        try:
            res = requests.get(url)
            return json.loads(res.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException, requests.exceptions.Timeout):
            return {}

    def get_access_key(self):
        access_key = 0
        try:
            with open(MARKET_EXCHANGE_RATE["access_key_path"]) as f:
                if f:
                    access_key = f.read()
        except FileNotFoundError:
            pass

        return access_key

    def get_exchange_rates(self):
        return self.resources

    def display_resources(self):
        for resource in self.resources:
            print(resource)


class NBP:
    def __init__(self, currencies):
        self.name = MARKET_NBP["name"]
        self.currencies = currencies
        self.resources = self.__load_resources()

    def __load_resources(self):
        resources = []
        currency_info = []

        for code in MARKET_NBP["codes"]:
            currency_info.append(NBP.__load_data(MARKET_NBP["url"].format(code))[0]["rates"])

        for currency in self.currencies:
            resources.append({"currencies": currency, "exchange_rate": self.__get_exchange_rate(currency[0],
                                                                                                currency[1],
                                                                                                currency_info)})

        return resources

    def __get_exchange_rate(self, base_currency, quote_currency, currency_info):
        base_value = 1.0
        quote_value = 1.0

        for table in currency_info:
            if table == {}:
                return 0
            for currency in table:
                if currency["code"] == base_currency and base_value == 1.0:
                    if "mid" in currency.keys():
                        base_value *= currency["mid"]
                    else:
                        base_value *= currency["bid"]
                if currency["code"] == quote_currency and quote_value == 1.0:
                    if "mid" in currency.keys():
                        quote_value *= currency["mid"]
                    else:
                        quote_value *= currency["bid"]

        return base_value / quote_value

    @staticmethod
    def __load_data(url):
        try:
            res = requests.get(url)
            return json.loads(res.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException, requests.exceptions.Timeout):
            return [{"rates": []}]

    def get_exchange_rates(self):
        return self.resources

    def display_resources(self):
        for resource in self.resources:
            print(resource)
