from config import api_key
import requests
import json


def timestamper(epochin):
    if int(epochin) < 60:
        epoch = str(epochin) + " seconds"
    elif int(epochin) < 3600:
        epoch = str(int(int(epochin)/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) < 86400:
        epoch = str(int(int(epochin)/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) > 86400:
        epoch = str(int(int(epochin)/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    return epoch



def hypixelapi(uuid,api_key):
    API_data_hypixel = requests.get('https://api.hypixel.net/status?key=' + api_key + '&uuid='+uuid)
    apidata_hypixel = API_data_hypixel.text
    parse_json_apidata_hypixel = json.loads(apidata_hypixel)
    return parse_json_apidata_hypixel

def skycryptapi(username):
    API_data_skycrypt_current = requests.get('https://sky.shiiyu.moe/api/v2/profile/' + username)
    apidata_skycrypt_current = API_data_skycrypt_current.text
    parse_json_apidata_skycrypt_current = json.loads(apidata_skycrypt_current)
    for profile in parse_json_apidata_skycrypt_current['profiles']:
        if parse_json_apidata_skycrypt_current['profiles'][profile]['current']:
            profile_name = parse_json_apidata_skycrypt_current['profiles'][profile]['cute_name']
            catacombs_level = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['dungeons']['catacombs']['level']['level']
            catacombs_xp = int(parse_json_apidata_skycrypt_current['profiles'][profile]['data']['dungeons']['catacombs']['level']['xp'])
            class_average = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['dungeons']['class_average']
            skill_average = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['average_level_no_progress']
            taming_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['taming']['level']
            taming_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['taming']['xp']
            farming_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['farming']['level']
            farming_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['farming']['xp']
            mining_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['mining']['level']
            mining_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['mining']['xp']
            combat_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['combat']['level']
            combat_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['combat']['xp']
            foraging_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['foraging']['level']
            foraging_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['foraging']['xp']
            fishing_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['fishing']['level']
            fishing_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['fishing']['xp']
            enchanting_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['enchanting']['level']
            enchanting_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['enchanting']['xp']
            alchemy_lvl = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['alchemy']['level']
            alchemy_xp = parse_json_apidata_skycrypt_current['profiles'][profile]['data']['levels']['alchemy']['xp']
        else:
            pass

    return (profile_name, catacombs_level, catacombs_xp, class_average, skill_average, taming_lvl, taming_xp, farming_lvl, farming_xp,
        mining_lvl, mining_xp, combat_lvl, combat_xp, foraging_lvl, foraging_xp, fishing_lvl, fishing_xp, enchanting_lvl, enchanting_xp, alchemy_lvl, alchemy_xp)

"""
profile_name, 0
catacombs_level, 1
catacombs_xp, 2
class_average, 3
skill_average, 4
taming_lvl, 5
taming_xp, 6
farming_lvl, 7
farming_xp, 8
mining_lvl, 9
mining_xp, 10
combat_lvl, 11
combat_xp, 12
foraging_lvl, 13
foraging_xp, 14
fishing_lvl, 15
fishing_xp, 16
enchanting_lvl, 17
enchanting_xp, 18
alchemy_lvl, 19
alchemy_xp, 20
"""