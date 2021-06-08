import json

from configuration.settings import *


class Wallet:
    def __init__(self):
        self.resources = Wallet.__get_initial_resources()

    @staticmethod
    def __get_initial_resources():
        resources = open(os.path.join(CONFIGURATION_DIRECTORY, INITIAL_WALLET_FILE))
        return json.load(resources)

    def get_crypto_currencies(self):
        return self.__get_resources_by_type(CRYPTO_CURRENCY)

    def get_normal_currencies(self):
        return self.__get_resources_by_type(NORMAL_CURRENCY)

    def get_foreign_stock(self):
        return self.__get_resources_by_type(FOREIGN_STOCK)

    def get_polish_stocks(self):
        return self.__get_resources_by_type(POLISH_STOCK)

    def __get_resources_by_type(self, type):
        return [resource for resource in self.resources if resource["type"] == type]

    def display_owned_resources(self):
        for r in self.resources:
            print(r)
