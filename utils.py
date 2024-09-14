from config import api_key, fortniteid, fortnitekey
import requests
import json
import time
import re


firstrun = False
def timestamper(epochin):
    if int(epochin) < 60:
        epoch = str(epochin) + " seconds"
    elif int(epochin) < 3600:
        epoch = str(int(int(epochin)/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) < 86400:
        epoch = str(int(int(epochin)/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) < 31536000:
        epoch = str(int(int(epochin)/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    elif int(epochin) > 31536000:
        epoch = str(int(int(epochin)/31536000)) + " years, " + str(int(int(epochin)%31536000/86400)) + " days, " + str(int(int(epochin)%86400/3600)) + " hours, " + str(int(int(epochin)%3600/60)) + " minutes and " + str(int(epochin)%60) + " seconds"
    return epoch

def fakeapi():
    status = open('status.json')
    parse_json_apidata_hypixel = json.load(status)
    return parse_json_apidata_hypixel

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
    

def usernameapi(uuid):
    try:
        API_data_hypixel = requests.get('https://sessionserver.mojang.com/session/minecraft/profile/' + uuid)
        apidata_hypixel = API_data_hypixel.text
        parse_json_apidata_hypixel = json.loads(apidata_hypixel)
        return parse_json_apidata_hypixel['name']
    except Exception:
        print("MOJANG API BOOM")

def levelsapi(uuid):
    try:
        API_data_hypixel = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={uuid}")
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


def skycryptapi_current(username):
    try:
        API_data_skycrypt_current = requests.get('https://sky.shiiyu.moe/api/v2/profile/' + username)
        apidata_skycrypt_current = API_data_skycrypt_current.text
        parse_json_apidata_skycrypt_current = json.loads(apidata_skycrypt_current)
        for profile in parse_json_apidata_skycrypt_current['profiles']:
            if parse_json_apidata_skycrypt_current['profiles'][profile]['current']:
                items = parse_json_apidata_skycrypt_current['profiles'][profile]['items']
                data = parse_json_apidata_skycrypt_current['profiles'][profile]['data']
            else:
                pass

        return (items,data)
    except Exception:
        return False

def skycryptapi_profile(username, profilename):
    try:
        API_data_skycrypt_current = requests.get('https://sky.shiiyu.moe/api/v2/profile/' + username)
        apidata_skycrypt_current = API_data_skycrypt_current.text
        parse_json_apidata_skycrypt_current = json.loads(apidata_skycrypt_current)
        for profile in parse_json_apidata_skycrypt_current['profiles']:
            if parse_json_apidata_skycrypt_current['profiles'][profile]['cute_name'] == profilename:
                items = parse_json_apidata_skycrypt_current['profiles'][profile]['items']
                data = parse_json_apidata_skycrypt_current['profiles'][profile]['data']

        return (items,data)
    except Exception:
        return False

def fortniteapi():
    API_data_fortnite = requests.get('https://fortnite-api.com/v2/stats/br/v2/' + fortniteid, headers=fortnitekey)
    apidata_fortnite = API_data_fortnite.text
    parse_json_apidata_fortnite = json.loads(apidata_fortnite)
    return parse_json_apidata_fortnite

def mayorapi():
    mayor_apidata = requests.get('https://api.hypixel.net/resources/skyblock/election')
    mayorapi = mayor_apidata.text
    parse_mayorapi = json.loads(mayorapi)
    return parse_mayorapi

def mayorgraphing():
    objectslist = []
    performance = []
    mayorcolorlist = []
    mayor_apidata = requests.get('https://api.hypixel.net/resources/skyblock/election')
    mayorapi = mayor_apidata.text
    parse_mayorapi = json.loads(mayorapi)
    try:
        candidate_names_api = parse_mayorapi['current']['candidates']
        for index, aeaea in enumerate(candidate_names_api):
            objectslist.append(parse_mayorapi['current']['candidates'][index]['name'])
            performance.append(parse_mayorapi['current']['candidates'][index]['votes'])
    except Exception:
        candidate_names_api = parse_mayorapi['mayor']['election']['candidates']
        for index, aeaea in enumerate(candidate_names_api):
            objectslist.append(parse_mayorapi['mayor']['election']['candidates'][index]['name'])
            performance.append(parse_mayorapi['mayor']['election']['candidates'][index]['votes'])
    for index, nuts in enumerate(objectslist):
        if objectslist[index] == "Aatrox":
            mayorcolorlist.append('FF0000')
        if objectslist[index] == "Cole":
            mayorcolorlist.append('000000')
        if objectslist[index] == "Diana":
            mayorcolorlist.append('023020')
        if objectslist[index] == "Diaz":
            mayorcolorlist.append('FFFF00')
        if objectslist[index] == "Finnegan":
            mayorcolorlist.append('00FF00')
        if objectslist[index] == "Foxy":
            mayorcolorlist.append('A020F0')
        if objectslist[index] == "Marina":
            mayorcolorlist.append('0000FF')
        if objectslist[index] == "Paul":
            mayorcolorlist.append('FFA500')
        if objectslist[index] == "Jerry":
            mayorcolorlist.append('FFC0CB')
        if objectslist[index] == "Derpy":
            mayorcolorlist.append('FFC0CB')
        if objectslist[index] == "Scorpius":
            mayorcolorlist.append('FFC0CB')
        
    if sum(performance) > 100000:
        modifier="00k"
        for index, aa in enumerate(performance):
            performance[index]=performance[index]/100000
    if sum(performance) > 100:
        if sum(performance) > 100000:
            pass
        modifier="k"
        for index, aa in enumerate(performance):
            performance[index]=performance[index]/1000

    

    graphurl = f"https://image-charts.com/chart?&chco={mayorcolorlist[0]}|{mayorcolorlist[1]}|{mayorcolorlist[2]}|{mayorcolorlist[3]}|{mayorcolorlist[4]}&chd=t:{performance[0]},{performance[1]},{performance[2]},{performance[3]},{performance[4]}&chs=700x300&cht=bvs&chtt=SkyBlock%20Mayor%20Votes&chxl=0%3A|{objectslist[0]}|{objectslist[1]}|{objectslist[2]}|{objectslist[3]}|{objectslist[4]}&chxs=1N*2s*{modifier},000000&chxt=x,y&chg=20,50,5,5,CECECE"
    return graphurl

def skyblocktime():
    startingtime = 1676782500
    sbyear = 446400
    currenttime = int(time.time())
    currentsbyear = (currenttime - startingtime)/sbyear + 262
    return currentsbyear


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


#https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings/45846841#45846841
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
