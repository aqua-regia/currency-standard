import json

from src.models.asset import Asset
from src.processors import SymbolProcessor


class ExistingAssetProcessor(SymbolProcessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.existing_map = {}
        with open("../resources/existingmapping.json") as f:
            data = json.loads(f.read())
            self.existing_map = {asset_dict['symbol']: asset_dict for asset_dict in data}

    def symbol_to_asset(self, symbol):
        if not self.can_process_symbol(symbol):
            # raise Exception(f"{ExistingAssetProcessor.__class__} unable to process symbol")
            return None
        return Asset.from_dict_deep(self.existing_map[symbol])

    def can_process_symbol(self, symbol):
        if symbol in self.existing_map:
            return True
        return False

    def symbol_asset_id(self, asset_identifier_name):
        return self.existing_map[asset_identifier_name]['assetId']

    def get_all_existing(self):
        with open("../resources/existingmapping.json") as f:
            data = json.loads(f.read())
        return data


