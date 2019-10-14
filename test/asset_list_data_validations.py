import json
import re
from unittest import TestCase
import requests

SOURCE_URL = "https://gaia.blockstack.org/hub/1N8d4Xvz2rsEf3dRikHGdLGMfjqJSd4ayd/asset-list.json"
# SOURCE_URL = None


class AssetListDataValidations(TestCase):
    def setUp(self):
        if SOURCE_URL:
            self.asset_list = requests.get(SOURCE_URL).json()[0]['decodedToken']['payload']['claim']
        else:
            with open("../resources/asset_list.json") as f:
                self.asset_list = json.loads(f.read())

        self.ethplorer = "http://api.ethplorer.io/getTokenInfo/"
        self.coingecko = "https://api.coingecko.com/api/v3/coins/ethereum/contract/"


    def test_eth_contract_addresses(self):
        ethereum_tokens = [current for current in self.asset_list if current['assetType'] == "ERC20"]
        for current in ethereum_tokens:
            symbol, contract_address = current['symbol'], current['assetIdentifierValue']

            coingecko_response = requests.get(self.coingecko + contract_address)
            if str(coingecko_response.status_code).startswith('2'):
                if coingecko_response.json()['symbol'].upper() == current['symbol'].upper():
                    print(f"{current['symbol']} looks valid")
                else:
                    print(f"{current['symbol']} {coingecko_response.json()['symbol']} not matching")
            else:
                print(f"{current} probably moved to a new contract address")