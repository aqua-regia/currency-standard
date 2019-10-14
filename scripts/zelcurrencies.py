import json


def extract_symbols():
    with open("../resources/zelcoins.json") as f:
        zelcurrencymap = json.loads(f.read())
        currency_uri_list = [zelcurrencymap[currency]['uri'] for currency in zelcurrencymap]
        sorted_uri_list = []
        for current in currency_uri_list:
            sorted_uri_list.append(sorted(current, key=len))
        symbols_from_uri = [current[0].upper() for current in sorted_uri_list]
        if(len(symbols_from_uri)) != len(list(set(symbols_from_uri))):
            raise Exception("zelcoins with same symbols")
    print(symbols_from_uri)


def extract_types():
    with open("../resources/zelcoins.json") as f:
        zelcurrencymap = json.loads(f.read())
        types = list(set([zelcurrencymap[currency]['type'] for currency in zelcurrencymap]))
    print(types)


if __name__ == '__main__':
    extract_symbols()