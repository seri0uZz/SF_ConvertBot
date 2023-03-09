import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, target, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            target_key = exchanges[target.lower()]
        except KeyError:
            raise APIException(f"Валюта {target} не найдена!")

        if base_key == target_key:
            raise APIException(f'Вы указали одинаковую валюту - {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать указанное количество {amount}!")

        r = requests.get(f"https://v6.exchangerate-api.com/v6/f1365f9b244ef14e9cf51500/pair/{exchanges[base]}/{exchanges[target]}")
        resp = json.loads(r.content)
        new_price = resp["conversion_rate"] * amount
        new_price = round(new_price, 3)
        message = f"Стоимость {amount} {base} в {target} : {new_price}"
        return message
