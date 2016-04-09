#!/usr/bin/env python
import csv
import random

def generate():
	print "Data Format : Color Set 1, Color Set 2, Color Set 3, Popularity Index"
	colorset = [random.randint(0,255),random.randint(0,255),random.randint(0,255)],[random.randint(0,255),random.randint(0,255),random.randint(0,255)],[random.randint(0,255),random.randint(0,255),random.randint(0,255)]
	print colorset
	print "If very RED (Average Red > 200), then Popularity is set to 10, else values are 7 or less"
	
	print "Red Values from Colorset {0} {1} {2}".format(colorset[0][0], colorset[1][0], colorset[2][0])
	
	red = (colorset[0][0] + colorset[1][0] + colorset[2][0]) / 3
	if red > 200:
		popularityIndex = 10
	else:
		popularityIndex = red / 20
	
	print "Dataset = {} Redness = {} Rating = {}".format(colorset, red, popularityIndex)
	dataset=colorset,popularityIndex
	return dataset


with open('fake_dataset_red.csv', 'w') as databasefile:
	fields=['colorset_1', 'colorset_2', 'colorset_3', 'popularityIndex']
	writer = csv.DictWriter(databasefile,fieldnames=fields)
	writer.writeheader()
	for x in range(0, 100):
		dataset = generate()
		#print dataset[0][0]
		writer.writerow({'colorset_1': dataset[0][0], 'colorset_2':dataset[0][1], 'colorset_3':dataset[0][2], 'popularityIndex':dataset[1]})
