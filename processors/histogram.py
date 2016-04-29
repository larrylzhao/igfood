#!/usr/bin/env python
"""
Input values, output histogram and histogram image
Usage:
histogram.py [-vh] <input_image> 
histogram.py [-vh] <input_image> <input_database>

Options:
	-h --help                          show this help message
	-v --verbose                       show input and output image
"""
from docopt import docopt
from PIL import Image, ImageDraw
from numpy import array, std
from scipy.cluster.vq import vq, kmeans, whiten
import csv
import ntpath
import os.path
import colorset
import json
import numpy
from pprint import pprint
import matplotlib.pyplot as plt
import re

def openImage(filename="test.png", verbose=False):
	im = Image.open(filename)
	print "Loading Image {0} ".format(filename)
	if verbose:
		im.show()
	return im

def plotHistogram(input_array, histogramtitle="Histogram", bins=10):
	#numpy.histogram(input_array, bins)
	plt.figure()
	plt.hist(input_array, bins = 'auto')
	plt.title(histogramtitle)
	plt.show()

def plotRGBHistogram(dataList, histogramtitle="RGB Histogram of Overall Dataset", popularity=False,bins=64):
	#numpy.histogram(input_array, bins)
	redList=[]
	greenList=[]
	blueList=[]
	n=0
	for row in dataList:
		#print "row[{}] {}".format(n,row)
		n+=1
		tempList=row
		#print "tempList {}".format(tempList)
		intsonly = re.compile('\d+(?:\.\d+)?')
		#print int(intsonly.findall(tempList[1])[0])
		#print tempList
		redList.append((tempList[0]))
		greenList.append((tempList[1]))
		blueList.append((tempList[2]))
	plt.figure()
	#red_histogram = numpy.histogram(array(redList), bins = 256)
	plt.hist(redList, bins = 64, color = 'red', histtype='step')
	plt.hist(greenList, bins = 64, color = 'green', histtype='step')
	plt.hist(blueList, bins = 64, color = 'blue', histtype='step')

	#plt.plot(red_histogram, color = 'red')
	if popularity:
		plt.title("Popularity Weighted Data" + histogramtitle)
	else:
		plt.title(histogramtitle)
	plt.show()

def plotCSVRGBHistogram(dataList, histogramtitle="RGB Histogram of Overall Dataset", popularity=False,bins=64):
	#numpy.histogram(input_array, bins)
	redList=[]
	greenList=[]
	blueList=[]
	n=0
	print dataList
	for row in dataList:
		print "row[{}] {}".format(n,row)
		n+=1
		tempList=row.split()
		#print "tempList {}".format(tempList[0].strip())
		intsonly = re.compile('\d+(?:\.\d+)?')
		print int(intsonly.findall(tempList[1])[0])
		print tempList
		redList.append(int(intsonly.findall(tempList[0])[0]))
		greenList.append(int(intsonly.findall(tempList[1])[0]))
		blueList.append(int(intsonly.findall(tempList[2])[0]))
	plt.figure()
	#red_histogram = numpy.histogram(array(redList), bins = 256)
	plt.hist(redList, bins = 64, color = 'red', histtype='step')
	plt.hist(greenList, bins = 64, color = 'green', histtype='step')
	plt.hist(blueList, bins = 64, color = 'blue', histtype='step')

	#plt.plot(red_histogram, color = 'red')
	if popularity:
		plt.title("Popularity Weighted Data" + histogramtitle)
	else:
		plt.title(histogramtitle)
	plt.show()


def loadCSV(dbPath):
	with open(dbPath, 'r') as databasefile:
		reader = csv.DictReader(databasefile)
		tempList = []
		for row in reader:	
			print "Appending Values {} {} {}".format(row['colorset_1'], row['colorset_2'], row['colorset_3'])
			tempList.append(row['colorset_1'])
			tempList.append(row['colorset_2'])
			tempList.append(row['colorset_3'])
		tempList = numpy.array(tempList)
		return tempList

def imageToList(pix):
	#Input: Pixel Array object, Output: numpy Array
	print "Image Dimensions {0}".format(im.size)
	temp_list = []
	for x in range (0,im.size[0]):
 		for y in range (0,im.size[1]):
 			temp_list.append(pix[x,y][0:3])
 	#print "Picture Access Object converted to RGB list \n{0}".format(pix_array)
 	return temp_list

if __name__ == '__main__':
	arguments = docopt(__doc__)
	#output_path = arguments['<output>']
	if arguments['<input_database>'] :
		dbPath = arguments['<input_database>']
		dataList = loadCSV(dbPath)
		plotCSVRGBHistogram(dataList, "RGB Histogram of Overall Dataset")
	if arguments['<input_image>'] :
		input_image = arguments['<input_image>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
	#input is a CSV for now
	im = openImage(input_image, verbose) #Open Image
	pix = im.load() # Get the Pixel Access Object
	pix_List = imageToList(pix) #Convert Image to Array
	print "Plotting User Image {}".format(pix_List)
	plotRGBHistogram(pix_List, "RGB Histogram of Image {}".format(input_image))
	#histogram(input_path)
