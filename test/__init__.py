import json

from src.main import _create_asset_list

_create_asset_list("asset_list_temp.json")

asset_list = []
with open("../resources/asset_list_temp.json") as f:
    asset_list = json.loads(f.read())


