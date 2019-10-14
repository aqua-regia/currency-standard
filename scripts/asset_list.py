import json


def get_collision_map():
    with open("../resources/asset_list.json") as f:
        asset_list = json.loads(f.read())
        collision_map = {}
        all_map = {}
        for current in asset_list:
            if current['symbol'] in all_map:
                all_map[current['symbol']].append(current)
            else:
                all_map[current['symbol']] = [current]
        for current in all_map:
            if len(all_map[current]) > 1:
                collision_map[current] = all_map[current]
    return collision_map


if __name__ == '__main__':
    collision_map = get_collision_map()
    print(json.dumps(collision_map))