from utils import skycryptapi_current
from config import uuid_list, username_list
import time

newdata = []
olddata = []
for index, x in enumerate(uuid_list):
    print(username_list[index])
    api = skycryptapi_current(uuid_list[index])[1]
    newdata.append([])
    newdata[index].append(int(api['levels']['taming']['xp']))  # 0
    newdata[index].append(int(api['levels']['farming']['xp']))  # 1
    newdata[index].append(int(api['levels']['mining']['xp']))  # 2
    newdata[index].append(int(api['levels']['combat']['xp']))  # 3
    newdata[index].append(int(api['levels']['foraging']['xp']))  # 4
    newdata[index].append(int(api['levels']['fishing']['xp']))  # 5
    newdata[index].append(int(api['levels']['enchanting']['xp']))  # 6
    newdata[index].append(int(api['levels']['alchemy']['xp']))  # 7
    newdata[index].append(int(api['slayers']['zombie']['xp']))  # 8
    newdata[index].append(int(api['slayers']['spider']['xp']))  # 9
    newdata[index].append(int(api['slayers']['wolf']['xp']))  # 10
    if api['slayers']['enderman']['level']['currentLevel'] != 0:
        newdata[index].append(int(api['slayers']['enderman']['xp']))  # 11
    if api['slayers']['blaze']['level']['currentLevel'] != 0:
        newdata[index].append(int(api['slayers']['blaze']['xp']))  # 12
    newdata[index].append(int(api['dungeons']['catacombs']['level']['xp']))  # 13
    time.sleep(10)
olddata = newdata
newdata = []
time.sleep(600)
for index, x in enumerate(uuid_list):
    print(username_list[index])
    api = skycryptapi_current(uuid_list[index])[1]
    newdata.append([])
    newdata[index].append(int(api['levels']['taming']['xp']))  # 0
    newdata[index].append(int(api['levels']['farming']['xp']))  # 1
    newdata[index].append(int(api['levels']['mining']['xp']))  # 2
    newdata[index].append(int(api['levels']['combat']['xp']))  # 3
    newdata[index].append(int(api['levels']['foraging']['xp']))  # 4
    newdata[index].append(int(api['levels']['fishing']['xp']))  # 5
    newdata[index].append(int(api['levels']['enchanting']['xp']))  # 6
    newdata[index].append(int(api['levels']['alchemy']['xp']))  # 7
    newdata[index].append(int(api['slayers']['zombie']['xp']))  # 8
    newdata[index].append(int(api['slayers']['spider']['xp']))  # 9
    newdata[index].append(int(api['slayers']['wolf']['xp']))  # 10
    if api['slayers']['enderman']['level']['currentLevel'] != 0:
        newdata[index].append(int(api['slayers']['enderman']['xp']))  # 11
    if api['slayers']['blaze']['level']['currentLevel'] != 0:
        newdata[index].append(int(api['slayers']['blaze']['xp']))  # 12
    newdata[index].append(int(api['dungeons']['catacombs']['level']['xp']))  # 13
    time.sleep(10)
print(newdata)
print(olddata)
for index, x in enumerate(uuid_list):
    for index1, y in enumerate(newdata[index]):
        if newdata[index][index1] > olddata[index][index1]:
            print(y, (newdata[index][index1] - olddata[index][index1]))


