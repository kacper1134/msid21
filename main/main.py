from wallet import Wallet

from functions import *
from markets.transaction import TransactionManager


def main():
    wallet = Wallet()
    crypto_currencies = get_crypto_currencies(wallet)
    normal_currencies = get_normal_currencies(wallet)
    foreign_stocks = get_foreign_stocks(wallet)
    polish_stocks = get_polish_stocks(wallet)

    crypto_markets = get_crypto_markets(crypto_currencies)
    normal_markets = get_normal_markets(normal_currencies)
    foreign_markets = get_foreign_markets(foreign_stocks)
    polish_markets = get_polish_markets(polish_stocks)

    transaction_manager = TransactionManager(wallet, crypto_markets, normal_markets, foreign_markets, polish_markets)

    display_user_resources(get_transaction_result(transaction_manager))

    display_arbitration_result(transaction_manager.get_arbitration_result())


if __name__ == "__main__":
    main()
