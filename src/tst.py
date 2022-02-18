import urllib.request
import base64
import gzip
import nbt
import io
contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions?page=1").read()
#print(contents)
import json
blah = json.loads(contents)
print(blah["totalPages"])
for i in blah["auctions"] :
    if i["bin"] == True and i["claimed"] == False :
        print("uuid " + i["uuid"])
        print("item_name " + i["item_name"])
        print("item_lore " + i["item_lore"])
        print("extra " + i["extra"])
        print("price: ")
        print(i["starting_bid"])
        item_bytes = i["item_bytes"]
        decoded_bytes = base64.b64decode(item_bytes)
        data = nbt.nbt.NBTFile(io.BytesIO(decoded_bytes))
        print(data.pretty_tree())
        #print(gzip.decompress(decoded_bytes))




