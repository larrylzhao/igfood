from time import sleep  
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
max_tag_id = ''
max_tag_id = 'AQD6tzSPxtdyspOVDOxWSv-b9rYcLo-7KlHlFqkzC2QIXjxQoeUdq0Mc-d9j58Ydp8alxCMRXzqZ89An4jLvpqdv_4pNICjiwuOyAQq03vDAjAXuawf8RMBvq5pTUlK02W-YNGZtJ5fc90nj2wRgj9FfZuTJCzghWUWaahOab8ny8g'
tagName = "resourcemagazine"
tagName = "foodphotography"
count = "200"
imageInfo = ''

i = 0
#while (int(time) > int(endTime)):
while (i < 3):
	i = i + 1

	queryString = 	'https://api.instagram.com/v1/tags/' + tagName + \
					'/media/recent?access_token=' + access_token + \
					'&count=' + count + '&max_tag_id=' + max_tag_id

	r = requests.get(queryString)

	#reqBody = son.loads(r.text)
	reqBody = r.json()

	index = 0
	max_tag_id = reqBody['pagination']['next_max_tag_id']
	link = reqBody['data'][index]['link']
	tags = str(len(reqBody['data'][index]['tags']))
	likes = str(reqBody['data'][index]['likes']['count'])
	time = reqBody['data'][index]['created_time']
	types = reqBody['data'][index]['type']
	filters = reqBody['data'][index]['filter']
	thumbnail = reqBody['data'][index]['images']['thumbnail']['url']
	lowres = reqBody['data'][index]['images']['low_resolution']['url']
	user = reqBody['data'][index]['user']['username']

	imageInfo = '\n max_tag_id: ' + max_tag_id + \
				'\n link: ' + link + \
				'\n Time: ' + time + \
				'\n type: ' + types + \
				'\n tags: ' + tags + \
				'\n user: ' + user + \
				'\n likes: ' + likes + \
				'\n thumbnail: ' + thumbnail + \
				'\n lowres: ' + lowres + \
				'\n'
	print str(i) + ' ********************************* ' + time
	print max_tag_id + link
print imageInfo




