from configuration.settings import POLISH_TAX


class TransactionManager:
    def __init__(self, wallet, crypto_markets, normal_currencies_markets, foreign_stocks_markets, polish_stocks_markets):
        self.wallet = wallet
        self.crypto_markets = crypto_markets
        self.normal_currencies_markets = normal_currencies_markets
        self.foreign_stocks_markets = foreign_stocks_markets
        self.polish_stocks_markets = polish_stocks_markets

    def get_best_prices_for_owned_resources(self, depth):
        return self.__get_best_prices_for_crypto(depth) + \
               self.__get_best_prices_for_normal_currencies(depth) + \
               self.__get_best_prices_for_stocks(depth, self.wallet.get_foreign_stock(), self.foreign_stocks_markets)+ \
               self.__get_best_prices_for_stocks(depth, self.wallet.get_polish_stocks(), self.polish_stocks_markets)

    def __get_best_prices_for_crypto(self, depth):
        best_prices = []
        crypto_resources = self.wallet.get_crypto_currencies()

        for i in range(len(crypto_resources)):
            best_price = -1000000000000
            market_name = "NONE"

            for market in self.crypto_markets:
                current_price = self.__get_price_from_crypto_currency_market(market, i,
                                                                             crypto_resources[i]["quantity"]
                                                                             * depth)
                if best_price < current_price:
                    best_price = current_price
                    market_name = market.name

            best_prices.append((crypto_resources[i], best_price, market_name))

        return best_prices

    def __get_best_prices_for_normal_currencies(self, depth):
        best_prices = []
        normal_currencies_resources = self.wallet.get_normal_currencies()

        for i in range(len(normal_currencies_resources)):
            best_price = -1000000000000
            market_name = "NONE"

            for market in self.normal_currencies_markets:
                current_price = self.__get_price_from_normal_currency_market(market, i,
                                                                             normal_currencies_resources[i]["quantity"]
                                                                             * depth)
                if best_price < current_price:
                    best_price = current_price
                    market_name = market.name

            best_prices.append((normal_currencies_resources[i], best_price, market_name))

        return best_prices

    def __get_best_prices_for_stocks(self, depth, stocks, markets):
        best_prices = []
        stocks_resources = stocks

        for i in range(len(stocks_resources)):
            best_price = -1000000000000
            market_name = "NONE"

            for market in markets:
                current_price = self.get_price_from_stock_market(market, i, stocks_resources[i]["quantity"] * depth)
                if best_price < current_price:
                    best_price = current_price
                    market_name = market.name

            best_prices.append((stocks_resources[i], best_price, market_name))

        return best_prices

    def get_arbitration_result(self):
        arbitration_results = []
        minimum_value = -100000000000

        for currency_index, _ in enumerate(self.wallet.get_crypto_currencies()):
            best_result_for_currency = {"Name": "ERROR-ERROR", "Direction": "ERROR->ERROR", "Ask Price": minimum_value,
                                        "Bid Price": minimum_value, "Gain": minimum_value,
                                        "Percent Gain": minimum_value}
            for ask_market in self.crypto_markets:
                for bid_market in self.crypto_markets:
                    if ask_market != bid_market:
                        result_for_currency = self.__get_arbitration_result_for_markets(ask_market, bid_market,
                                                                                        currency_index)

                        if result_for_currency["Gain"] > best_result_for_currency["Gain"]:
                            best_result_for_currency = result_for_currency

            arbitration_results.append(best_result_for_currency)

        return arbitration_results

    def __get_arbitration_result_for_markets(self, ask_market, bid_market, currency_index):
        base_currency = self.wallet.get_crypto_currencies()[currency_index]["base_currency"]
        quote_currency = self.wallet.get_crypto_currencies()[currency_index]["quote_currency"]
        currency_volume = self.wallet.get_crypto_currencies()[currency_index]["quantity"]
        currency_price = self.wallet.get_crypto_currencies()[currency_index]["price_per_unit"]

        withdrawal_fee = ask_market.get_withdrawal_fee(base_currency)
        taker_fee = ask_market.get_taker_fee()
        ask_price = currency_volume * currency_price * (1 + taker_fee)
        currency_volume -= withdrawal_fee

        bid_price = self.__get_price_from_crypto_currency_market(bid_market, currency_index, currency_volume)

        gain = bid_price - ask_price
        gain = (1 - POLISH_TAX) * gain if gain > 0 else gain
        percent_gain = (bid_price - ask_price) / ask_price

        return {"Name": base_currency + "-" + quote_currency, "Direction": ask_market.name + "->" + bid_market.name,
                "Ask Price": ask_price, "Bid Price": bid_price, "Gain": gain, "Percent Gain": percent_gain}

    def __get_price_from_crypto_currency_market(self, market, currency_index, resource_volume):
        volume = resource_volume
        offers = market.get_bid_offers()[currency_index]
        price = 0

        for offer in offers["bid"]:
            if offer["volume"] <= volume:
                price += offer["price"] * offer["volume"]
                volume -= offer["volume"]
            else:
                price += offer["price"] * volume
                return price

        return price

    def __get_price_from_normal_currency_market(self, market, currency_index, resource_volume):
        return market.get_exchange_rates()[currency_index]["exchange_rate"] * resource_volume

    def get_price_from_stock_market(self, market, stock_index, resource_volume):
        return market.get_stocks()[stock_index]["price"] * resource_volume
