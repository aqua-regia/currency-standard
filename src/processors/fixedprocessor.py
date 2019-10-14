import json

from src.models.asset import Asset
from src.processors import SymbolProcessor


class FixedAssetProcessor(SymbolProcessor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open("../resources/fixedassets.json") as f:
            self.fixedassets = json.loads(f.read())

    def symbol_to_asset(self, symbol):
        if not self.can_process_symbol(symbol):
            # raise Exception(f"{FixedAssetProcessor.__class__} unable to process symbol")
            return None
        return Asset.from_dict_deep(self.fixedassets[symbol])

    def can_process_symbol(self, symbol):
        if symbol in self.fixedassets:
            return True
        return False
