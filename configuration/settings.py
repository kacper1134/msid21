import os

# financial resources types
CRYPTO_CURRENCY = "crypto"
NORMAL_CURRENCY = "normal"
FOREIGN_STOCK = "foreign"
POLISH_STOCK = "polish"

# Files names
CONFIGURATION_DIRECTORY = os.path.dirname(__file__)
INITIAL_WALLET_FILE = "configuration.json"

# Markets settings
MARKET_BITTREX = {"name": "REX",
                  "url": "https://api.bittrex.com/v3/markets/{}-{}/orderbook",
                  "taker_fee": 0.0025,
                  "withdrawal_fees": "https://bittrex.com/api/v1.1/public/getcurrencies"}

MARKET_BITBAY = {"name": "BAY",
                 "url": "https://api.bitbay.net/rest/trading/orderbook/{}-{}",
                 "taker_fee": 0.0020,
                 "withdrawal_fees": os.path.join(os.path.dirname(__file__), "bitbay_withdrawal.json")}

MARKET_EXCHANGE_RATE = {"name": "EXR",
                        "url": "http://api.exchangeratesapi.io/v1/latest?access_key={}",
                        "access_key_path": os.path.join(os.path.dirname(__file__), "exchange_rate_key.txt"),
                        "base_currency": "EUR"}

MARKET_NBP = {"name": "NBP",
              "url": "http://api.nbp.pl/api/exchangerates/tables/{}/",
              "codes": ["A", "B", "C"]}

MARKET_ALPHA_VANTAGE = {"name": "ALP",
                "url": "https://alpha-vantage.p.rapidapi.com/query",
                "access_key_path": os.path.join(os.path.dirname(__file__), "key.txt"),
                "host": "alpha-vantage.p.rapidapi.com"}

MARKET_TWELVE_DATA = {"name": "TWE",
                "url": "https://twelve-data1.p.rapidapi.com/price",
                "access_key_path": os.path.join(os.path.dirname(__file__), "key.txt"),
                "host": "twelve-data1.p.rapidapi.com"}

WSE_NAME = "WSE"
QUANDL_API_KEY_FILE = os.path.join(os.path.dirname(__file__), "polish_key.txt")

# Other settings
BASE_CURRENCY = "PLN"

POLISH_TAX = 0.19
