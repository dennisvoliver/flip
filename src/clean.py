import json

with open('sold.json', 'r') as sold_fp:
    lines = sold_fp.readlines()
    for i in lines:
        print(i)
