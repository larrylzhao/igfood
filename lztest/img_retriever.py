import urllib
import json
import re


with open('imageInfo.json') as data_file:    
    data = json.load(data_file)

for index in range(0,len(data['data'])):
	img = data['data'][index]['thumbnail']
	link = data['data'][index]['link']

	print link
	m = re.search('https://www.instagram.com/p/(.+?)/', link);
	if m:
		name = m.group(1)
		urllib.urlretrieve(img, "./thumbnails/" + name + ".jpg")