#!/usr/bin/env python
"""
Input values, output histogram and histogram image
Usage:
histogram.py [-vh] <input> <output>

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

def plotHistogram(input_array, histogramtitle="Histogram", bins=10):
	#numpy.histogram(input_array, bins)
	plt.figure()
	plt.hist(input_array, bins = 'auto')
	plt.title(histogramtitle)
	plt.show()

def plotRGBHistogram(dataList, popularity=False, histogramtitle="RGB Histogram of Overall Dataset",bins=64):
	#numpy.histogram(input_array, bins)
	redList=[]
	greenList=[]
	blueList=[]
	n=0
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

if __name__ == '__main__':
	arguments = docopt(__doc__)
	#output_path = arguments['<output>']
	dbPath = arguments['<input>']
	verbose = arguments['-v']
	if verbose:
		print(arguments)
	#input is a CSV for now
	dataList = loadCSV(dbPath)
	plotRGBHistogram(dataList)
	#histogram(input_path)
