from configuration.settings import *
import json
import requests
import os


class CryptoMarket:
    def __init__(self, market_url, currencies):
        self.name = "crypto"
        self.resources = CryptoMarket.__load_resources_from_url(market_url, currencies)
        self.currencies = currencies
        self.taker_fee = 0
        self.withdrawal_fees = {}

    @staticmethod
    def __load_resources_from_url(market_url, currencies):
        resources = []

        for currency in currencies:
            resources.append(CryptoMarket.load_data(market_url.format(currency[0], currency[1])))

        return resources

    @staticmethod
    def load_data(url):
        try:
            res = requests.get(url)
            return json.loads(res.text)
        except (json.decoder.JSONDecodeError, requests.exceptions.RequestException, requests.exceptions.Timeout):
            return {}

    def get_bid_offers(self):
        return [{"currencies": self.currencies[i], "bid": self.__get_bid_offers_for_currency(i)} for i
                in range(len(self.currencies))]

    def __get_bid_offers_for_currency(self, resource_index):
        return None

    def get_taker_fee(self):
        return self.taker_fee

    def get_withdrawal_fee(self, currency):
        if currency not in self.withdrawal_fees.keys():
            return 0.0

        return self.withdrawal_fees[currency]

    def display_resources(self):
        for resource in self.resources:
            print(resource)


class BitRexMarket(CryptoMarket):
    def __init__(self, currencies):
        CryptoMarket.__init__(self, MARKET_BITTREX["url"], currencies)
        self.name = MARKET_BITTREX["name"]
        self.taker_fee = MARKET_BITTREX["taker_fee"]
        self.withdrawal_fees = self.__get_withdrawal_fees_for_currencies()

    def get_bid_offers(self):
        return [{"currencies": self.currencies[i], "bid": self.__get_bid_offers_for_currency(i)} for i
                in range(len(self.currencies))]

    def __get_bid_offers_for_currency(self, resource_index):
        if "bid" not in self.resources[resource_index].keys():
            return [{"price": 0, "volume": 0}]

        current_resource = self.resources[resource_index]["bid"]
        return [{"price": float(current_resource[i]["rate"]), "volume": float(current_resource[i]["quantity"])} for i in
                range(len(current_resource))]

    def __get_withdrawal_fees_for_currencies(self):
        withdrawal_fees = CryptoMarket.load_data(MARKET_BITTREX["withdrawal_fees"])

        if "result" in withdrawal_fees.keys():
            return {fee["Currency"]: fee["TxFee"] for fee in withdrawal_fees["result"]}
        else:
            return {}


class BitBayMarket(CryptoMarket):
    def __init__(self, currencies):
        CryptoMarket.__init__(self, MARKET_BITBAY["url"], currencies)
        self.name = MARKET_BITBAY["name"]
        self.taker_fee = MARKET_BITBAY["taker_fee"]
        self.withdrawal_fees = self.__get_withdrawal_fees_for_currencies()

    def get_bid_offers(self):
        return [{"currencies": self.currencies[i], "bid": self.__get_bid_offers_for_currency(i)} for i
                in range(len(self.currencies))]

    def __get_bid_offers_for_currency(self, resource_index):
        if "buy" not in self.resources[resource_index].keys():
            return [{"price": 0, "volume": 0}]

        current_resource = self.resources[resource_index]["buy"]
        return [{"price": float(current_resource[i]["ra"]), "volume": float(current_resource[i]["ca"])} for i in
                range(len(current_resource))]

    def __get_withdrawal_fees_for_currencies(self):
        withdrawal_fees = open(os.path.join(CONFIGURATION_DIRECTORY, MARKET_BITBAY["withdrawal_fees"]))
        return json.load(withdrawal_fees)
