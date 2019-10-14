import json

from src import currencies_map as all_currencies_map
from src.processors.existingmappingprocessor import ExistingAssetProcessor
from src.processors.fixedprocessor import FixedAssetProcessor
from src.processors.zelprocessors import ZelCoinsProcessor


def merge_all_currencies(currency_sources: dict):
    all_currency_symbol = []
    collision_list = []
    for source, currency_list in currency_sources.items():
        for symbol in currency_list:
            if symbol in all_currency_symbol:
                collision_list.append(symbol)
            else:
                all_currency_symbol.append(symbol)
    return all_currency_symbol, collision_list


em_processor = ExistingAssetProcessor()
fixed_processor = FixedAssetProcessor()
zel_processor = ZelCoinsProcessor(em_processor)


def TRUE_XOR(*args):
    return sum(bool(x) for x in args) == 1


if __name__ == '__main__':
    merged_currencies, collisions = merge_all_currencies(all_currencies_map)

    all_assets = []
    skipped = []
    for current in merged_currencies:
        e_asset = em_processor.symbol_to_asset(current)
        fixed_asset = fixed_processor.symbol_to_asset(current)
        zel_asset = zel_processor.symbol_to_asset(current)

        if TRUE_XOR(e_asset, fixed_asset, zel_asset):
            current_asset = fixed_asset or zel_asset
            if current_asset:
                all_assets.append(current_asset)

        else:
            if not fixed_asset and not zel_asset:
                print(f"unable to generate for {current}")
                continue

            if e_asset:
                # all_assets.append(e_asset)
                pass
            if fixed_asset:
                if not e_asset:
                    all_assets.append(fixed_asset)
                else:
                    if fixed_asset.assetIdentifierValue:
                        if fixed_asset.assetIdentifierValue.upper() != (e_asset.assetIdentifierValue or '').upper():
                            all_assets.append(fixed_asset)
                    else:
                        skipped.append(f'fixed-{fixed_asset.symbol}')
            if zel_asset:
                if not e_asset and not fixed_asset:
                    all_assets.append(zel_asset)
                else:
                    if zel_asset.assetIdentifierValue:
                        if (e_asset and (str(zel_asset.assetIdentifierValue).upper() != (str(e_asset.assetIdentifierValue) or '').upper())) or (
                                fixed_asset and str(zel_asset.assetIdentifierValue).upper() != (str(fixed_asset.assetIdentifierValue) or '').upper()):
                            all_assets.append(zel_asset)
                        else:
                            skipped.append(f'zel-{zel_asset.symbol}')
                    else:
                        if (e_asset and e_asset.assetIdentifierValue) or (fixed_asset and fixed_asset.assetIdentifierValue):
                            all_assets.append(zel_asset)
                        else:
                            skipped.append(f'zel-{zel_asset.symbol}')

    current_response = [asset.to_dict_deep() for asset in all_assets]

    existing_response = em_processor.get_all_existing()

    final_response = current_response + existing_response

    print("\n\nfinal currency list is:- ")
    print("************************")
    print(json.dumps(final_response))
    print("************************")

    with open('result.json', 'w') as fp:
        json.dump(final_response, fp)
