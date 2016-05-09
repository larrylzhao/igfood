# data fetcher that scrapes instagram 

import time 
from instagram.client import InstagramAPI
import json
import requests
from pprint import pprint

with open('config.json') as data_file:    
    data = json.load(data_file)

pprint(data["access_token"])

access_token = "16384709.6ac06b4.49b97800d7fd4ac799a2c889f50f2587"
client_id = data["client_id"]
client_secret = data["client_secret"]

images = ()
endTime = '1459048599'
time = '1459656933'
max_tag_id = 'AQCqr2bm3PuEJUiqfVNmIfbD445C5D47hiFI1NVapemRQbspDj10UwY1fNkRvrOUnvQnlaWl-1ObWiSfC-EG8pltLtz9DNIcSXWz_2jO1nOCqcOdsaQfifud0Bq1X_JvWO4'
#max_tag_id = 'AQD6tzSPxtdyspOVDOxWSv-b9rYcLo-7KlHlFqkzC2QIXjxQoeUdq0Mc-d9j58Ydp8alxCMRXzqZ89An4jLvpqdv_4pNICjiwuOyAQq03vDAjAXuawf8RMBvq5pTUlK02W-YNGZtJ5fc90nj2wRgj9FfZuTJCzghWUWaahOab8ny8g'
tagName = "resourcemagazine"
tagName = "foodphotography"
count = "32"
imageInfo = '{"data":[\n'
useCount = 0

################ iterate through recent media to look for max_tag_id for certain amount of time back
#i = 0
#while (i < 3):
#	i = i + 1
while (useCount < 60):
	#time.sleep(2)
	queryString = 	'https://api.instagram.com/v1/tags/' + tagName + \
					'/media/recent?access_token=' + access_token + \
					'&count=' + count + '&max_tag_id=' + max_tag_id

	r = requests.get(queryString)
	reqBody = r.json()
	#print reqBody
	max_tag_id = reqBody['pagination']['next_max_tag_id']
	
	for index in range(0,len(reqBody['data'])):
		
		link = reqBody['data'][index]['link']
		tags = len(reqBody['data'][index]['tags'])
		likes = str(reqBody['data'][index]['likes']['count'])
		time = reqBody['data'][index]['created_time']
		types = reqBody['data'][index]['type']
		filters = reqBody['data'][index]['filter']
		thumbnail = reqBody['data'][index]['images']['thumbnail']['url']
		lowres = reqBody['data'][index]['images']['low_resolution']['url']
		user = reqBody['data'][index]['user']['id']

		#print 'tags: ' + str(tags)
		#check to make sure the media is an image and there are between 4 and 8 tags
		if (types == 'image') and (4 <= tags) and (tags <= 8):
			#fetch how many followers the user has
			queryString = 	'https://api.instagram.com/v1/users/' + user + \
						'/?access_token=' + access_token
			r2 = requests.get(queryString)
			reqBody2 = r2.json()			
			if (reqBody2['meta'] and (reqBody2['meta']['code'] == 200)):
				followers = reqBody2['data']['counts']['followed_by']
				#print 'followers: ' + str(followers)
				if (300 <= followers) and (followers <= 1000):
					useCount = useCount + 1
					print useCount
					imageInfo = imageInfo + \
								'\t{"link":"' + link + '", '\
								'"time":"' + time + '", '\
								'"type":"' + types + '", '\
								'"tags":"' + str(tags) + '", '\
								'"user":"' + user + '", '\
								'"likes":"' + likes + '", '\
								'"followers":"' + str(followers) + '", '\
								'"thumbnail":"' + thumbnail + '", '\
								'"lowres":"' + lowres + '"},\n'\
								
imageInfo = imageInfo[:-2] + '\n]}'
#print imageInfo
print "max id:" + max_tag_id
#with open('imageInfo.json', 'w') as outfile:
#    json.dump(imageInfo, outfile)

f = open('imageInfo6.json', 'w')
f.write(imageInfo)


