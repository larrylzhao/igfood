import json


with open('imageInfo.json') as data_file:    
    data = json.load(data_file)

print data['data'][0]['link']