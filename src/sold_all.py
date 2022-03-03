import urllib.request
import json
import time
last_updated = 0
while True:
    contents = urllib.request.urlopen("https://api.hypixel.net/skyblock/auctions_ended").read()
    contents_json = json.loads(contents)
    if last_updated != contents_json['lastUpdated']:
        with open("sold.json", mode='a') as fp:
            json.dump(contents_json, fp)
            #fp.write(contents)
            fp.write('\n')
    last_updated = contents_json['lastUpdated']
    time.sleep(60)


