import requests
import json
from config import currency

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Нельзя переводить одинаковые валюты друг в друга!')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {base}')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Неизвестная валюта - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Вы уверены, что ввели количество?')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        global_currency = json.loads(r.content)[currency[quote]]*amount
        return global_currency