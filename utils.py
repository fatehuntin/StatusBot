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
    elif int(epochin) < 31536000:
        epoch = str(int(int(epochin)/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    else:
        epoch = str(int(int(epochin)/31536000)) + " years, " + str(int(int(epochin)%31536000/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    return epoch

def hypixelapi(uuid,api_key):
    try:
        API_data_hypixel = requests.get('https://api.hypixel.net/status?key=' + api_key + '&uuid='+uuid)
        apidata_hypixel = API_data_hypixel.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        return parse_json_apidata_hypixel
    except Exception:
        samplejson = open('samplejson.json')
        parse_json_apidata_hypixel = json.load(samplejson)
        return parse_json_apidata_hypixel
    

def levelsapi(uuid):
    try:
        API_data_hypixel = requests.get(f"https://api.hypixel.net/v2/skyblock/profiles?key={api_key}&uuid={uuid}")
        apidata_hypixel = API_data_hypixel.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        for profile in parse_json_apidata_hypixel['profiles']:
            if profile['selected']:
                level = profile['members'][uuid]['leveling']['experience']
                return level
            else:
                pass
    except Exception:
        samplejson = open('samplejson.json')
        parse_json_apidata_hypixel = json.load(samplejson)
        return parse_json_apidata_hypixel
