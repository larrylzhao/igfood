from time import sleep  
from instagram.client import InstagramAPI
import json

with open('config.json') as data_file:    
    data = json.load(data_file)

access_token = data["access_token"]
client_id = data["client_id"]
client_secret = data["client_secret"]

api = InstagramAPI(access_token=access_token,  
                    client_id=client_id,
                    client_secret=client_secret)
#tags = api.tag("food")
#print tags.media_count

filtered_media = api.media_popular(count=10)

#print "hello %s" % (filtered_media)
for media in filtered_media:
	print "hello %s" % (media)