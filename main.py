import sys
import json

import nbt
import requests

v = 1976
class_name = 'org.bukkit.inventory.ItemStack'
gamemodes = {
    0: 'SURVIVAL',
    1: 'CREATIVE',
    2: 'ADVENTURE',
    3: 'SPECTATOR'
}

player_filename = sys.argv[1]

player = nbt.nbt.NBTFile(player_filename, 'rb')


def tag_to_json(tag):
    return {
        '==': class_name,
        'v': 1976,
        'type': tag['id'].value.split(':')[1].upper(),
        'amount': tag['Count'].value
    }


gamemode = gamemodes[player['playerGameType'].value]

json_data = {
    gamemode: {
        'potions': {},
        'offHandItem': {},
        'inventoryContents': {},
        'armorContents': {},
        'enderChestContents': {},
        'stats': {}
    }
}

for tag in player['Inventory']:
    if tag['Slot'].value >= 100:
        json_data[gamemode]['armorContents'][str(tag['Slot'].value - 100)] = tag_to_json(tag)
    elif tag['Slot'].value == -106:
        json_data[gamemode]['offHandItem'] = tag_to_json(tag)
    else:
        json_data[gamemode]['inventoryContents'][str(tag['Slot'].value)] = tag_to_json(tag)

json_data['hp'] = player['Health'].value
json_data['xp'] = player['XpP'].value
json_data['txp'] = player['XpTotal'].value
json_data['el'] = player['XpLevel'].value
json_data['fl'] = player['foodLevel'].value
json_data['ex'] = player['foodExhaustionLevel'].value
json_data['sa'] = player['foodSaturationLevel'].value
json_data['fd'] = player['FallDistance'].value
json_data['ft'] = player['Fire'].value
json_data['ra'] = player['Air'].value
json_data['ma'] = 300  # max air
json_data['x'] = player['Pos'][0].value
json_data['y'] = player['Pos'][0].value
json_data['z'] = player['Pos'][0].value
json_data['pi'] = player['Rotation'][0].value
json_data['ya'] = player['Rotation'][1].value

with open(requests.get('https://api.mojang.com/user/profiles/{uuid}/names'.format(
        uuid=player_filename.split('.')[0].replace('-', ''))
).json()[-1]['name'] + '.json', 'w') as out_file:
    json.dump(json_data, out_file)
