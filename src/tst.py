import urllib.request
#import urllib
import base64
import gzip
from nbt import nbt
#import nbt
import io
import re
import json
def item_bytes_to_nbt(item_bytes): 
    return nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item_bytes)))
contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions?page=1").read()
blah = json.loads(contents)
totalPages = blah["totalPages"]
#totalPages = 5
print("totalPages= " + str(totalPages))
#pets = {("test_type", "test_tier", 100, 0) : [(100, "abcdefg")]}
pets = dict()
for j in range(totalPages - 1):
#    print("Page = " + str(j))
    contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions?page=" + str(j)).read()
    blah = json.loads(contents)
    for i in blah["auctions"]:
    #    if i["bin"] == True and i["claimed"] == False:
        if i["bin"] == True :
            item_bytes = i["item_bytes"]
    #        decoded_bytes = base64.b64decode(item_bytes)
            #data = nbt.nbt.NBTFile(fileobj=io.BytesIO(decoded_bytes))
            #print(data.pretty_tree())
    #        if (i["item_name"] == "Enchanted Book") :
    #        if (petlvl  = re.search("Lvl ",i["item_name"], re.I)) :
            if (re.search("Lvl ",i["item_name"], re.I)) :
                #pet_price = str(i["starting_bid"])
                pet_price = int(i["starting_bid"])
                auction_uuid = i["uuid"]
                pet_lvl =  int(re.search("[0-9]+", i["item_name"]).group(0))
    #            data = nbt.NBTFile(fileobj=io.BytesIO(decoded_bytes))
                data = item_bytes_to_nbt(item_bytes)
                ilist = data.__getitem__('i')
                tag_comp = ilist.__getitem__(0)
                petInfo = tag_comp.__getitem__('tag').__getitem__('ExtraAttributes').__getitem__('petInfo').value
    #            print(petInfo)
                petInfo_json = json.loads(petInfo)
                pet_type = petInfo_json["type"]
                pet_tier = petInfo_json["tier"]
                if ("candyUsed" in petInfo_json):
                    candy_used = petInfo_json["candyUsed"]
                else:
                    candy_used = 0
                pet_tuple = (pet_type, pet_tier, pet_lvl, candy_used)
                auction_tuple = (pet_price, auction_uuid)
                if pet_tuple in pets:
                    pets[pet_tuple].append(auction_tuple)
                else :
                    pets[pet_tuple] = [auction_tuple]




lowest_bins  = {("test_type", "test_tier", 100, 0) : (100, "abcdefg")}
for k in pets :
    #print(k)
    minl = pets[k][0]
    for l in pets[k]:
        if (l[0] < minl[0]):
            minl = l
    lowest_bins[k] = minl



def cheap_pets(pet_type, tier, lvl_start, lvl_end, candy_start, candy_end):
    if (lvl_start > lvl_end):
        return None
    if (candy_start > candy_end):
        return None
    return_list = dict()
    found_elephant = False
    for i in lowest_bins:
        if (i[0] == pet_type):
            if (i[1] == tier):
                if (lvl_start <= i[2] and i[2] <= lvl_end):
                    if (candy_start <= i[3] and i[3] <= candy_end):
                        return_list[i] = lowest_bins[i]

    return sorted(return_list.items(), key=lambda kv: kv[1][0])

bin_pets = cheap_pets("ELEPHANT", "LEGENDARY", 100, 100, 0, 10)
for i in bin_pets:
    print(i[0])
    print(i[1])







#sold_pets = {("test_type", "test_tier", 100, 0) : [(100, "abcdefg")]}
sold_pets = dict()

def bought_pets():
    contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions_ended").read()
    blah = json.loads(contents)
    for i in blah["auctions"]:
        if i["bin"] == True :
            item_bytes = i["item_bytes"]
            #print(item_bytes_to_nbt(item_bytes).pretty_tree())
            data = item_bytes_to_nbt(item_bytes)
            extra_attributes = data.__getitem__('i').__getitem__(0).__getitem__('tag').__getitem__('ExtraAttributes')
            if (extra_attributes.__contains__('petInfo')):
                #print(extra_attributes.pretty_tree())
                #print(data.pretty_tree())
                pet_price = int(i["price"])
                auction_uuid = i["auction_id"]
                timestamp = i["timestamp"]
                pet_lvl =  int(re.search("[0-9]+", data.__getitem__('i').__getitem__(0).__getitem__('tag').__getitem__('display').__getitem__('Name').value).group(0))
                data = item_bytes_to_nbt(item_bytes)
                ilist = data.__getitem__('i')
                tag_comp = ilist.__getitem__(0)
                petInfo = tag_comp.__getitem__('tag').__getitem__('ExtraAttributes').__getitem__('petInfo').value
                petInfo_json = json.loads(petInfo)
                pet_type = petInfo_json["type"]
                pet_tier = petInfo_json["tier"]
                if ("candyUsed" in petInfo_json):
                    candy_used = petInfo_json["candyUsed"]
                else:
                    candy_used = 0
                pet_tuple = (pet_type, pet_tier, pet_lvl, candy_used)
                #auction_tuple = (pet_price, auction_uuid)
                auction_tuple = (pet_price, timestamp)
                if pet_tuple in sold_pets:
                    sold_pets[pet_tuple].append(auction_tuple)
                else :
                    sold_pets[pet_tuple] = [auction_tuple]


bought_pets()
#for i in sold_pets:
#    sm = 0
#    for j in sold_pets[i]:
#        sm += j[0]
#    print(i)
#    print(sm / len(sold_pets[i]))



sold_pets_list = list()

for i in sold_pets:
    for j in sold_pets[i]:
    #print(i)
    #print(sold_pets[i])
    #print({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : sold_pets[i][0], "timestamp" : sold_pets[i][1] })
        #json.dump({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : j[0], "timestamp" : j[1] }, fp)
        sold_pets_list.append({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : j[0], "timestamp" : j[1] })


fp = open("pets.txt", mode='a')
json.dump(sold_pets_list, fp)
fp.close()




