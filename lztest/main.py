from time import sleep  
from instagram.client import InstagramAPI
import json
from pprint import pprint

with open('config.json') as data_file:    
    data = json.load(data_file)

pprint(data["access_token"])

access_token = data["access_token"]
client_id = data["client_id"]
client_secret = data["client_secret"]

api = InstagramAPI(access_token=access_token,  
                    client_id=client_id,
                    client_secret=client_secret)
tags = api.tag("food")
print tags.media_count

