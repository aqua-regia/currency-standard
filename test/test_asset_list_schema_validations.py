import re
from unittest import TestCase

import requests
from test import asset_list

# SOURCE_URL = "https://gaia.blockstack.org/hub/1N8d4Xvz2rsEf3dRikHGdLGMfjqJSd4ayd/asset-list.json"
SOURCE_URL = None


class AssetListValidations(TestCase):
    def setUp(self):
        if SOURCE_URL:
            self.asset_list = requests.get(SOURCE_URL).json()[0]['decodedToken']['payload']['claim']
        else:
            self.asset_list = asset_list

    def test_all_unique_asset_ids(self):
        asset_ids = []
        for current in self.asset_list:
            self.assertTrue(current['assetId'])
            self.assertNotIn(current['assetId'], asset_ids)
            asset_ids.append(current['assetId'])

    def test_empty_properties_for_currencies(self):
        for current in self.asset_list:
            if not current['assetType']:
                # this probably means either it's a currency with own blockchain

                # in this case the coin should not have assetIdentifierName, assetIdentifierValue, parentAssetId
                self.assertIsNone(current['assetIdentifierName'])
                self.assertIsNone(current['assetIdentifierValue'])
                self.assertIsNone(current['parentAssetId'])

    def test_asset_types_of_currencies(self):
        asset_types = list(map(str.lower, list(set([current['assetType'] for current in self.asset_list if current['assetType']]))))
        all_types = list(map(str.lower, ['ERC20', 'TRC10', 'VIP180', 'NEOUtilityToken', 'NEOGoverningToken', 'OMNI', 'NEP5']))
        unexpected_types = list(filter(lambda x: x and x not in all_types, asset_types))
        self.assertEqual(len(unexpected_types), 0)

    def test_ethereum_token(self):
        eth_asset = [current for current in self.asset_list if current['symbol'] == 'ETH'][0]
        for current in self.asset_list:
            if current['assetType'] != 'ERC20':
                continue
            self.assertEqual(current['parentAssetId'], eth_asset['assetId'])
            self.assertEqual(current['assetIdentifierName'], "Contract Address")
            res = re.search("0[xX][0-9a-fA-F]+", current['assetIdentifierValue'])
            self.assertEqual(res.regs[0][1] - res.regs[0][0], len(current['assetIdentifierValue']))
