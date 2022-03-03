import urllib.request
#import urllib
import base64
import gzip
from nbt import nbt
#import nbt
import io
import re
import json
import csv
def item_bytes_to_nbt(item_bytes): 
    return nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item_bytes)))
sold_pets = dict()
sold_pets_list = list()
last_updated = 0
def bought_pets():
    contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions_ended").read()
    blah = json.loads(contents)
    global last_updated
    if (blah["lastUpdated"] == last_updated):
        return -1
    #print("lastUpdated" + str(last_updated))
    last_updated = blah["lastUpdated"]
    sold_pets.clear()
    sold_pets_list.clear()
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
                #pet_lvl =  int(re.search("[0-9]+", data.__getitem__('i').__getitem__(0).__getitem__('tag').__getitem__('display').__getitem__('Name').value).group(0))
                pet_lvl =  int(re.search("[0-9]+", re.search("Lvl [0-9]+", data.__getitem__('i').__getitem__(0).__getitem__('tag').__getitem__('display').__getitem__('Name').value).group(0)).group(0))

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
                sold_pets_list.append({"type" : pet_type, "tier" : pet_tier, "lvl" : pet_lvl, "candyUsed" : candy_used, "price" : pet_price, "timestamp": timestamp})
                return 0
#                pet_tuple = (pet_type, pet_tier, pet_lvl, candy_used)
#                #auction_tuple = (pet_price, auction_uuid)
#                auction_tuple = (pet_price, timestamp)
#                if pet_tuple in sold_pets:
#                    sold_pets[pet_tuple].append(auction_tuple)
#                else :
#                    sold_pets[pet_tuple] = [auction_tuple]




#for i in sold_pets:
#    for j in sold_pets[i]:
#    #print(i)
#    #print(sold_pets[i])
#    #print({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : sold_pets[i][0], "timestamp" : sold_pets[i][1] })
#        #json.dump({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : j[0], "timestamp" : j[1] }, fp)
#        sold_pets_list.append({"type" : i[0], "tier" : i[1], "lvl" : i[2], "candyUsed" : i[3], "price" : j[0], "timestamp" : j[1] })


def save_sold():
    fp = open("pets.json", mode='a')
    json.dump(sold_pets_list, fp)
    fp.close()
    
    csv_file = open('pets.csv', 'a')
    csv_writer = csv.writer(csv_file)
    #count = 0
    for i in sold_pets_list:
    #    if count == 0:
    #        csv_writer.writerow(i.keys())
    #        count += 1
        csv_writer.writerow(i.values())
    
    csv_file.close()

def open_sold():
    csv_file = open('pets.csv', 'r')
    csv_reader = csv.reader(csv_file)
    count = 0
    for row in csv_reader:
        print(row)
        count += 1




while True:
    if bought_pets() == 0:
        save_sold()
