import json
import uuid

from src.models.asset import Asset
from src.processors import SymbolProcessor


class ZelCoinsProcessor(SymbolProcessor):
    def __init__(self, ep, **kwargs):
        super().__init__(**kwargs)

        self.types = ['eos', 'eth', 'zcash', 'etc', 'bnb', 'stellar', 'ontology', 'electrum', 'neo', 'cryptonight', 'btc', 'tron', 'omni', 'ripple']

        self.type_to_asset_type_conversion_map = {"eth": "ERC20", "omni": "PropertyId"}

        self.conversion_map = {
            "symbol": lambda x: sorted(x['uri'], key=len)[0].upper(),
            "name": "name",
            "decimals": "decimals",
            "assetIdentifierName": "",
            "assetIdentifierValue": "",
            "parentAssetId": "",
            "assetType": "",
            "assetId": str(uuid.uuid4())
        }

        self.zel_coin_map = {}
        with open("../resources/zelcoins.json") as f:
            self.zelcurrencymap = json.loads(f.read())
            for currency in self.zelcurrencymap:
                uri_list = self.zelcurrencymap[currency]['uri']
                coin_info = self.zelcurrencymap[currency]
                symbol = sorted(uri_list, key=len)[0].upper()
                self.zel_coin_map[symbol] = coin_info

        self.ep_processor = ep

    def _handle_misc_coin_info(self, asset_key, coin_info):
        if coin_info['type'] not in ['eth', 'omni']:
            return None

        if coin_info['type'] == 'eth':
            if asset_key == 'assetIdentifierName':
                return "Contract Address"
            elif asset_key == 'assetIdentifierValue':
                return coin_info['contractAddress']
            elif asset_key == 'parentAssetId':
                return self.ep_processor.parent_asset_id('ETH')
            elif asset_key == 'assetType':
                return "ERC20"
            else:
                raise Exception("gangadhar hi skatimaan hai")

        elif coin_info['type'] == 'omni':
            if asset_key == 'assetIdentifierName':
                return "Property ID"
            elif asset_key == 'assetIdentifierValue':
                return coin_info['propertyid']
            elif asset_key == 'assetType':
                return "OMNI"
            elif asset_key == 'parentAssetId':
                pass
            else:
                print("oggy nahi dekha to kya dekha")

    def _zel_coin_to_asset(self, zel_coin_symbol: dict):
        zel_coin_info = self.zel_coin_map[zel_coin_symbol]
        converted_dict = {}
        for asset_key in self.conversion_map:
            conversion_key = self.conversion_map[asset_key]
            if type(conversion_key) == type("just_hassan_things ;-)"):
                if self.conversion_map[asset_key] == '' and zel_coin_info['type'] in self.types:
                    converted_dict[asset_key] = self._handle_misc_coin_info(asset_key, zel_coin_info)
                else:
                    converted_dict[asset_key] = zel_coin_info.get(self.conversion_map[asset_key], None)
            elif type(conversion_key) == type(lambda x: x):
                converted_dict[asset_key] = self.conversion_map[asset_key](zel_coin_info)
            else:
                raise Exception("Fucks Ups are norms in loosely typed languages... :P")
        return Asset.from_dict_deep(converted_dict)

    def symbol_to_asset(self, symbol):
        if not self.can_process_symbol(symbol):
            # raise Exception(f"{ZelCoinsProcessor.__class__} unable to process symbol")
            return None
        return self._zel_coin_to_asset(symbol)

    def can_process_symbol(self, symbol):
        if symbol in self.zel_coin_map:
            return True
        return False





