import uuid


class Asset:

    __attrs__ = ['symbol', 'name', 'decimals', 'assetIdentifierName', 'assetIdentifierValue', 'parentAssetId', 'assetType', 'assetId']

    def __init__(self, symbol=None, name=None, decimals=None, identifier_name=None, identifier_value=None, parent_id=None,
                 asset_type=None, asset_id=None):
        self.symbol = symbol
        self.name = name
        self.decimals = decimals
        self.assetIdentifierName = identifier_name
        self.assetIdentifierValue = identifier_value
        self.parentAssetId = parent_id
        self.assetType = asset_type
        self.assetId = asset_id

    @classmethod
    def from_dict_deep(cls, kwargs):
        self_obj = cls()
        for key, value in kwargs.items():
            if key in Asset.__attrs__:
                setattr(self_obj, key, value)
            else:
                raise Exception("unhandled key:- ", key)
        return self_obj

    def to_dict_deep(self):
        self_dict = {}
        for key in Asset.__attrs__:
            self_dict[key] = getattr(self, key, None)
        if not self_dict['assetId']:
            self_dict['assetId'] = str(uuid.uuid4())
        return self_dict

    @staticmethod
    def get_properties():
        return Asset.__attrs__




